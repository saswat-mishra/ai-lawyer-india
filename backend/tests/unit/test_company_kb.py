"""Company KB ingestion + cross-device isolation."""
import pytest

from app.db import store
from app.ingest.company_ingest import ingest_company_doc


@pytest.mark.asyncio
async def test_text_doc_ingestion_creates_chunks():
    raw = "This is our internal NDA template. Confidential.\n\nClause 1: Mutual disclosure...".encode()
    doc = await store.insert_company_document(
        device_id="dev-A", filename="nda.txt", mime_type="text/plain",
        size_bytes=len(raw),
    )
    n = await ingest_company_doc(doc_id=doc["id"], device_id="dev-A",
                                    raw_bytes=raw, mime_type="text/plain", filename="nda.txt")
    assert n >= 1
    chunks = await store.list_company_chunks("dev-A")
    assert len(chunks) >= 1


@pytest.mark.asyncio
async def test_cross_device_isolation():
    raw_a = b"Device A confidential content."
    raw_b = b"Device B confidential content."
    doc_a = await store.insert_company_document(
        device_id="dev-A", filename="a.txt", mime_type="text/plain",
        size_bytes=len(raw_a))
    doc_b = await store.insert_company_document(
        device_id="dev-B", filename="b.txt", mime_type="text/plain",
        size_bytes=len(raw_b))
    await ingest_company_doc(doc_id=doc_a["id"], device_id="dev-A",
                                 raw_bytes=raw_a, mime_type="text/plain",
                                 filename="a.txt")
    await ingest_company_doc(doc_id=doc_b["id"], device_id="dev-B",
                                 raw_bytes=raw_b, mime_type="text/plain",
                                 filename="b.txt")
    chunks_a = await store.list_company_chunks("dev-A")
    chunks_b = await store.list_company_chunks("dev-B")
    assert all(c["device_id"] == "dev-A" for c in chunks_a)
    assert all(c["device_id"] == "dev-B" for c in chunks_b)
    # Texts must not bleed.
    assert not any("Device B" in c["text"] for c in chunks_a)
    assert not any("Device A" in c["text"] for c in chunks_b)


@pytest.mark.asyncio
async def test_delete_cascades_chunks():
    raw = b"Some content for deletion test."
    doc = await store.insert_company_document(
        device_id="dev-A", filename="d.txt", mime_type="text/plain",
        size_bytes=len(raw))
    await ingest_company_doc(doc_id=doc["id"], device_id="dev-A",
                                 raw_bytes=raw, mime_type="text/plain",
                                 filename="d.txt")
    chunks_before = await store.list_company_chunks("dev-A")
    assert chunks_before
    ok = await store.delete_company_document(doc["id"], "dev-A")
    assert ok
    chunks_after = await store.list_company_chunks("dev-A")
    assert chunks_after == []
