"""Source drill-down routes. Used by the citation pill drawer."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import store

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("/chunk/{chunk_id}")
async def get_chunk(chunk_id: str) -> dict:
    chunk = await store.get_legal_chunk(chunk_id)
    if not chunk:
        raise HTTPException(404, "chunk not found")
    doc = await store.get_legal_document(chunk["document_id"])
    return {
        "chunk": chunk,
        "document": doc,
    }


@router.get("/successor")
async def successor(act: str, section: str) -> dict:
    m = await store.lookup_successor_section(act, section)
    if not m:
        return {"found": False}
    return {"found": True, **m}


@router.get("/cited_by")
async def cited_by(citation: str, limit: int = 50) -> dict:
    """Return cases that cite the given case. Useful for the citator drawer:
    'who has followed / distinguished / overruled this judgment?'."""
    from app.rag import citator
    rows = await citator.cited_by(citation, limit=limit)
    return {"citation": citation, "count": len(rows), "results": rows}


@router.get("/cites")
async def cites(citation: str, limit: int = 50) -> dict:
    """What does this case cite?"""
    docs = await store.list_legal_documents()
    target = next((d for d in docs if (d.get("short_citation") or "").strip() == citation.strip()), None)
    if not target:
        return {"citation": citation, "count": 0, "results": []}
    rows = await store.list_citations_from(source_doc_id=target["id"], limit=limit)
    return {"citation": citation, "count": len(rows), "results": rows}
