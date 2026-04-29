"""Qdrant Cloud / self-hosted store — Phase 2-ready, dormant in Phase 1.

Drop-in module for the legal-corpus vector index when the corpus outgrows the
in-memory bundle. Activated when env var QDRANT_URL is set; otherwise import
is a no-op so tests and current deploy stay on the existing JSONL backend.

Free-tier sizing (Apr 2026): Qdrant Cloud free cluster is 1 GB RAM / 4 GB
disk forever. With binary quantisation (~128 B per 1024-dim vector) that
fits ~1 M vectors. For our scope (top-100 cases + Constitution + ~30 active
acts at full bare-act depth ≈ 5-10 K chunks), the free tier is comfortable.

Public surface mirrors the subset of `app.db.store` we need at retrieval
time. Idempotent upsert by chunk_id.
"""
from __future__ import annotations

import os
from typing import Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qm
    _QDRANT_AVAILABLE = True
except ImportError:  # qdrant-client is optional until Phase 2 activates this
    QdrantClient = None  # type: ignore[assignment]
    qm = None  # type: ignore[assignment]
    _QDRANT_AVAILABLE = False


COLLECTION = "legal_chunks"


def is_enabled() -> bool:
    """True when this store should be used instead of the in-memory one."""
    return _QDRANT_AVAILABLE and bool(os.environ.get("QDRANT_URL", "").strip())


def _client() -> "QdrantClient":
    if not _QDRANT_AVAILABLE:
        raise RuntimeError("qdrant-client not installed")
    url = os.environ.get("QDRANT_URL")
    api_key = os.environ.get("QDRANT_API_KEY")
    return QdrantClient(url=url, api_key=api_key, prefer_grpc=False, timeout=10)


def ensure_collection(*, dim: int = 1536) -> None:
    """Idempotent: create the collection with binary quantisation if missing."""
    c = _client()
    existing = {col.name for col in c.get_collections().collections}
    if COLLECTION in existing:
        return
    c.create_collection(
        collection_name=COLLECTION,
        vectors_config=qm.VectorParams(size=dim, distance=qm.Distance.COSINE),
        # Binary quantisation: ~30x storage compression, recall recovered by
        # rescore on the top-200 candidates with full-precision vectors.
        quantization_config=qm.BinaryQuantization(
            binary=qm.BinaryQuantizationConfig(always_ram=True)
        ),
        # HNSW index params tuned for legal corpus recall.
        hnsw_config=qm.HnswConfigDiff(m=16, ef_construct=100),
    )
    # Payload indexes for the filters we use most.
    for field, ftype in [
        ("act_short", "keyword"),
        ("section_number", "keyword"),
        ("status", "keyword"),
        ("jurisdiction", "keyword"),
    ]:
        c.create_payload_index(
            collection_name=COLLECTION,
            field_name=field,
            field_schema=ftype,
        )


def upsert_chunks(rows: list[dict[str, Any]]) -> int:
    """Upsert prebuilt chunks (with embedding vectors) into Qdrant.
    Each row needs: id, embedding, text, metadata."""
    c = _client()
    points = [
        qm.PointStruct(
            id=row["id"],
            vector=row["embedding"],
            payload={
                "text": row["text"],
                "section_number": row.get("section_number"),
                "act_short": row.get("metadata", {}).get("act_short"),
                "status": row.get("status", "in_force"),
                "jurisdiction": row.get("jurisdiction", "india"),
                "hierarchy_path": row.get("hierarchy_path"),
                "chunk_type": row.get("chunk_type"),
                "document_id": row.get("document_id"),
            },
        )
        for row in rows
    ]
    c.upsert(collection_name=COLLECTION, points=points, wait=True)
    return len(points)


async def hybrid_search(
    query_vector: list[float], *,
    query_text: str | None = None,
    limit: int = 50,
    must_filters: dict | None = None,
    must_not_filters: dict | None = None,
) -> list[dict[str, Any]]:
    """Vector + payload-filtered search. With binary quantisation we run a
    rescore stage automatically inside Qdrant so recall stays close to fp32.
    """
    c = _client()
    f_must = []
    f_must_not = []
    for k, v in (must_filters or {}).items():
        f_must.append(qm.FieldCondition(key=k, match=qm.MatchValue(value=v)))
    for k, v in (must_not_filters or {}).items():
        if isinstance(v, list):
            for item in v:
                f_must_not.append(
                    qm.FieldCondition(key=k, match=qm.MatchValue(value=item))
                )
        else:
            f_must_not.append(qm.FieldCondition(key=k, match=qm.MatchValue(value=v)))
    qfilter = qm.Filter(must=f_must or None, must_not=f_must_not or None)
    res = c.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=limit,
        query_filter=qfilter,
        with_payload=True,
        # Rescore the top binary-quantised candidates with the full-precision
        # vectors before returning — recovers ~5 % recall@10.
        search_params=qm.SearchParams(quantization=qm.QuantizationSearchParams(
            ignore=False, rescore=True, oversampling=2.0,
        )),
    )
    return [
        {
            "id": p.id,
            "score": p.score,
            **(p.payload or {}),
        }
        for p in res
    ]
