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
