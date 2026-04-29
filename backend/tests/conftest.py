"""Shared pytest fixtures."""
from __future__ import annotations

import asyncio
import os

import pytest

# Force the in-memory backend for tests; ensure no API key bleeds in.
os.environ["AIL_FORCE_MEMORY"] = "1"
os.environ.setdefault("DEVICE_COOKIE_SECRET", "test-secret-with-enough-entropy-12345")
os.environ.setdefault("OPENAI_API_KEY", "")  # mock path
os.environ.setdefault("APP_ENV", "test")


@pytest.fixture(autouse=True)
def _reset_store():
    from app.db import store
    store.reset_for_tests()
    yield
    store.reset_for_tests()


@pytest.fixture
async def seeded():
    """Seed the corpus so retrieval has data."""
    from app.ingest.legal_seed import seed_legal_corpus
    await seed_legal_corpus()


@pytest.fixture
def app():
    from app.main import create_app
    return create_app()


@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
async def seeded_client(seeded, app):
    from fastapi.testclient import TestClient
    return TestClient(app)
