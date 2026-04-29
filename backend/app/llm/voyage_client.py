"""Voyage AI embedding client — Phase 2-ready, dormant in Phase 1.

Voyage's `voyage-law-2` is purpose-built for legal text and consistently
beats general-purpose embeddings on legal recall benchmarks. Free tier:
50 M tokens for voyage-law-2 (more than enough for our top-100 cases +
Constitution + 30 active acts at full bare-act depth).

Activation in Phase 2:
    1. Set VOYAGE_API_KEY env var.
    2. Set EMBEDDING_BACKEND=voyage.
    3. Re-run scripts/build_corpus.py to re-embed at 1024 dim.
    4. Update Qdrant collection dim to 1024 (or use a separate collection).

Falls back to OpenAI in Phase 1 when env vars are absent.
"""
from __future__ import annotations

import os
from typing import Iterable


VOYAGE_LAW_MODEL = "voyage-law-2"
VOYAGE_LAW_DIM = 1024


def is_enabled() -> bool:
    if os.environ.get("EMBEDDING_BACKEND", "").lower() != "voyage":
        return False
    return bool(os.environ.get("VOYAGE_API_KEY", "").strip())


async def embed(texts: list[str], *, model: str = VOYAGE_LAW_MODEL,
                  input_type: str = "document") -> list[list[float]]:
    """Batch-embed `texts` via the Voyage API.

    `input_type` should be 'document' for corpus chunks and 'query' for the
    user's question — Voyage uses asymmetric prompts to improve retrieval.
    """
    try:
        import httpx
    except ImportError:
        raise RuntimeError("httpx required for Voyage client")
    api_key = os.environ.get("VOYAGE_API_KEY")
    if not api_key:
        raise RuntimeError("VOYAGE_API_KEY not set")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.voyageai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"input": texts, "model": model, "input_type": input_type},
        )
        resp.raise_for_status()
        data = resp.json()
    return [d["embedding"] for d in data["data"]]
