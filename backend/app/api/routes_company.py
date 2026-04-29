"""Company knowledge base routes. Per-device, never cross-visible."""
from __future__ import annotations

import io
from typing import Annotated

from fastapi import (APIRouter, File, Form, HTTPException, Request, Response,
                       UploadFile)

from app.api.schemas import CompanyDocOut, CompanyLinkRequest
from app.core.device import device_id_from_request, get_or_create_device_id
from app.db import store
from app.ingest.company_ingest import ingest_company_doc, ingest_company_link

router = APIRouter(prefix="/api/company", tags=["company"])

ALLOWED_MIME = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
    "text/markdown",
    "text/csv",
    "image/png",
    "image/jpeg",
    "image/webp",
}
MAX_BYTES = 50 * 1024 * 1024  # 50 MB


@router.post("/docs", response_model=CompanyDocOut)
async def upload_doc(file: Annotated[UploadFile, File()],
                      doc_type: Annotated[str, Form()] = "agreement",
                      request: Request = None,
                      response: Response = None) -> CompanyDocOut:
    device_id = get_or_create_device_id(request, response)
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(415, f"unsupported mime type {file.content_type}")
    raw = await file.read()
    if len(raw) > MAX_BYTES:
        raise HTTPException(413, f"file too large (max {MAX_BYTES} bytes)")
    safe_name = _sanitise_filename(file.filename or "document")
    doc = await store.insert_company_document(
        device_id=device_id,
        filename=safe_name,
        mime_type=file.content_type,
        size_bytes=len(raw),
        doc_type=doc_type,
    )
    # Synchronously ingest so the user sees `ready` quickly. For huge files
    # this would move to a background worker.
    try:
        await ingest_company_doc(doc_id=doc["id"], device_id=device_id,
                                    raw_bytes=raw, mime_type=file.content_type,
                                    filename=safe_name)
        await store.update_company_document_status(doc["id"], "ready")
        doc["status"] = "ready"
    except Exception as e:
        await store.update_company_document_status(doc["id"], "failed")
        doc["status"] = "failed"
        doc.setdefault("metadata", {})["error"] = str(e)[:200]
    return CompanyDocOut(**{
        "id": doc["id"], "filename": doc["filename"], "mime_type": doc["mime_type"],
        "size_bytes": doc["size_bytes"], "doc_type": doc["doc_type"],
        "status": doc["status"], "link_url": doc.get("link_url"),
        "created_at": doc["created_at"],
    })


@router.post("/links", response_model=CompanyDocOut)
async def add_link(req: CompanyLinkRequest, request: Request,
                    response: Response) -> CompanyDocOut:
    device_id = get_or_create_device_id(request, response)
    doc = await store.insert_company_document(
        device_id=device_id,
        filename=req.label or req.url,
        mime_type="text/url",
        size_bytes=len(req.url),
        doc_type="link",
        link_url=req.url,
    )
    try:
        await ingest_company_link(doc_id=doc["id"], device_id=device_id,
                                    url=req.url, label=req.label)
        await store.update_company_document_status(doc["id"], "ready")
        doc["status"] = "ready"
    except Exception as e:
        await store.update_company_document_status(doc["id"], "failed")
        doc["status"] = "failed"
    return CompanyDocOut(**{
        "id": doc["id"], "filename": doc["filename"], "mime_type": doc["mime_type"],
        "size_bytes": doc["size_bytes"], "doc_type": doc["doc_type"],
        "status": doc["status"], "link_url": doc.get("link_url"),
        "created_at": doc["created_at"],
    })


@router.get("/docs", response_model=list[CompanyDocOut])
async def list_docs(request: Request) -> list[CompanyDocOut]:
    device_id = device_id_from_request(request)
    if not device_id:
        return []
    docs = await store.list_company_documents(device_id)
    return [CompanyDocOut(**{
        "id": d["id"], "filename": d["filename"], "mime_type": d["mime_type"],
        "size_bytes": d["size_bytes"], "doc_type": d["doc_type"],
        "status": d["status"], "link_url": d.get("link_url"),
        "created_at": d["created_at"],
    }) for d in docs]


@router.delete("/docs/{doc_id}")
async def delete_doc(doc_id: str, request: Request) -> dict:
    device_id = device_id_from_request(request)
    if not device_id:
        raise HTTPException(401, "no session")
    ok = await store.delete_company_document(doc_id, device_id)
    if not ok:
        raise HTTPException(404, "doc not found")
    return {"ok": True}


def _sanitise_filename(name: str) -> str:
    import re
    name = name.replace("\\", "/").split("/")[-1]
    return re.sub(r"[^A-Za-z0-9._\- ]", "_", name)[:200]
