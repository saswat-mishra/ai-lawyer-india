"""Phase 1 infrastructure modules — must import cleanly + stay dormant
without env vars."""
import os


def test_qdrant_store_dormant_by_default(monkeypatch):
    monkeypatch.delenv("QDRANT_URL", raising=False)
    from app.db import qdrant_store
    assert qdrant_store.is_enabled() is False


def test_voyage_client_dormant_by_default(monkeypatch):
    monkeypatch.delenv("EMBEDDING_BACKEND", raising=False)
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    from app.llm import voyage_client
    assert voyage_client.is_enabled() is False


def test_voyage_client_dormant_without_key(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "voyage")
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    from app.llm import voyage_client
    assert voyage_client.is_enabled() is False


def test_voyage_client_active_when_both_set(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "voyage")
    monkeypatch.setenv("VOYAGE_API_KEY", "vk-fake")
    from app.llm import voyage_client
    assert voyage_client.is_enabled() is True
    monkeypatch.delenv("EMBEDDING_BACKEND")
    monkeypatch.delenv("VOYAGE_API_KEY")
