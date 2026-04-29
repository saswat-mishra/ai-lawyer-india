"""LLM-as-reranker behaviour."""
import os

import pytest

from app.rag.rerank import is_enabled, rerank
from app.rag.retriever import RetrievedChunk


def _chunk(i: int, text: str = "") -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=f"c-{i}", document_id="d", text=text or f"chunk {i}",
        chunk_type="section", section_number=str(i),
        hierarchy_path=["X", f"§{i}"], score=1.0 - i * 0.01,
        cosine=0.5 - i * 0.01, lexical=0.0, source_kind="legal",
    )


def test_disabled_when_env_off(monkeypatch):
    monkeypatch.delenv("RERANK_ENABLED", raising=False)
    assert is_enabled() is False


def test_disabled_without_openai_key(monkeypatch):
    monkeypatch.setenv("RERANK_ENABLED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    # Reload settings since they're cached.
    from app.core.config import get_settings
    get_settings.cache_clear()
    assert is_enabled() is False


@pytest.mark.asyncio
async def test_passthrough_when_at_or_below_top_k():
    chunks = [_chunk(i) for i in range(3)]
    out = await rerank("query", chunks, top_k=8)
    assert out == chunks  # unchanged when already <= top_k


@pytest.mark.asyncio
async def test_returns_top_k_at_most():
    chunks = [_chunk(i) for i in range(20)]
    # With no API key the function falls back to original ordering, clipped.
    out = await rerank("any query", chunks, top_k=8)
    assert len(out) == 8


@pytest.mark.asyncio
async def test_no_loss_of_chunks():
    """Even on fallback, every returned chunk must be from the input set."""
    chunks = [_chunk(i) for i in range(20)]
    out = await rerank("any query", chunks, top_k=12)
    for c in out:
        assert c in chunks
