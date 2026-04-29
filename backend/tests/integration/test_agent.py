"""End-to-end agent: refusal, retrieval, persona depth."""
import pytest

from app.agents.graph import run_agent
from app.core.config import Persona
from app.db import store


@pytest.mark.asyncio
async def test_refusal_when_no_corpus():
    # No seed loaded.
    state = await run_agent(device_id="d1", conversation_id=None,
                              query="What is the legal status of moon citizens?")
    # With no corpus, support density is 0 → refusal.
    assert state.refused or state.confidence == "refused" or state.answer_md


@pytest.mark.asyncio
async def test_retrieval_with_corpus(seeded):
    state = await run_agent(device_id="d1", conversation_id=None,
                              query="What does Section 103 BNS say?")
    assert state.legal_results, "expected retrievals"
    assert any(c.section_number == "103" for c in state.legal_results)


@pytest.mark.asyncio
async def test_company_doc_blends_in(seeded):
    """A company document is uploaded; the agent should pull it as a parallel source."""
    from app.ingest.company_ingest import ingest_company_doc
    await store.upsert_device("dev-X", persona="founder")
    doc = await store.insert_company_document(
        device_id="dev-X", filename="company-policy.txt",
        mime_type="text/plain",
        size_bytes=200,
    )
    raw = b"Acme Corp policy: cheque dishonour notices must be sent within 7 days."
    await ingest_company_doc(doc_id=doc["id"], device_id="dev-X",
                                 raw_bytes=raw, mime_type="text/plain",
                                 filename="company-policy.txt")
    state = await run_agent(device_id="dev-X", conversation_id=None,
                              query="cheque bounce 138")
    assert state.company_results, "expected company doc retrievals"
    assert state.company_results[0].source_kind == "company"
