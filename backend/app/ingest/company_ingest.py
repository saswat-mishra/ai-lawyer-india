"""Company doc ingestion: extract -> chunk -> embed -> store (per-device namespace)."""
from __future__ import annotations

import asyncio
from typing import Iterable

import httpx

from app.db import store
from app.ingest.text_extract import extract_text
from app.llm.openai_client import embed
from app.rag.chunker import chunk_freeform


async def ingest_company_doc(*, doc_id: str, device_id: str, raw_bytes: bytes,
                                mime_type: str, filename: str) -> int:
    """Ingest a single uploaded company doc. Returns chunk count."""
    text = extract_text(raw_bytes, mime_type, filename)
    if not text.strip():
        return 0
    chunks = chunk_freeform(text, source=filename, max_tokens=600)
    embeddings = await embed([c.text for c in chunks])
    for chunk, vec in zip(chunks, embeddings):
        await store.insert_company_chunk(
            document_id=doc_id, device_id=device_id,
            page=None, text=chunk.text,
            token_count=chunk.token_count(),
            embedding=vec,
            metadata={"source_filename": filename, "chunk_type": chunk.chunk_type},
        )
    return len(chunks)


async def ingest_company_link(*, doc_id: str, device_id: str, url: str,
                                  label: str = "") -> int:
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        resp = await client.get(url, headers={"User-Agent": "AILawyerIndia/0.1"})
        resp.raise_for_status()
        ct = resp.headers.get("content-type", "text/html").split(";")[0].strip()
    body = resp.text if ct.startswith("text/") else ""
    if ct.startswith("text/html"):
        body = _html_to_text(body)
    if not body.strip():
        return 0
    chunks = chunk_freeform(body, source=label or url, max_tokens=600)
    embeddings = await embed([c.text for c in chunks])
    for chunk, vec in zip(chunks, embeddings):
        await store.insert_company_chunk(
            document_id=doc_id, device_id=device_id,
            page=None, text=chunk.text,
            token_count=chunk.token_count(),
            embedding=vec,
            metadata={"source_url": url, "chunk_type": "link"},
        )
    return len(chunks)


def _html_to_text(html: str) -> str:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return html
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text("\n", strip=True)
