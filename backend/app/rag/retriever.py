"""Hybrid retrieval — dense (cosine) + lexical (token overlap), fused via RRF.

In production this calls the `hybrid_search_legal` Postgres function. In the
in-memory dev/test backend, we re-implement the same behaviour over Python lists.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

from app.core.config import Persona, get_settings
from app.db import store
from app.llm.openai_client import embed


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    text: str
    chunk_type: str
    section_number: str | None
    hierarchy_path: list[str]
    score: float                # fused RRF score (used for ordering)
    cosine: float = 0.0         # raw dense cosine similarity (used for quality / refusal floor)
    lexical: float = 0.0        # bm25-ish overlap
    source_kind: str = "legal"  # "legal" or "company"
    metadata: dict = field(default_factory=dict)


_LEGAL_STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "and", "or", "is", "are", "be", "by",
    "for", "with", "any", "such", "shall", "may", "section", "act", "this",
    "that", "shall", "as", "from", "on", "all", "no", "not",
}


def _tokenize(text: str) -> list[str]:
    return [
        t for t in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if t not in _LEGAL_STOPWORDS and len(t) > 1
    ]


def _cosine(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    num = sum(a[i] * b[i] for i in range(n))
    da = math.sqrt(sum(x * x for x in a)) or 1.0
    db = math.sqrt(sum(x * x for x in b)) or 1.0
    return num / (da * db)


def _bm25ish(query_tokens: list[str], chunk_text: str) -> float:
    """Cheap BM25-ish lexical score: token overlap weighted by inverse-frequency-ish.
    Sufficient for dev / small corpus tests; replaced by Postgres ts_rank in prod.
    """
    chunk_tokens = _tokenize(chunk_text)
    if not chunk_tokens or not query_tokens:
        return 0.0
    chunk_set = set(chunk_tokens)
    overlap = sum(1 for t in query_tokens if t in chunk_set)
    return overlap / max(1, len(query_tokens))


def _rrf_fuse(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal rank fusion. `rankings` is a list of lists, each list a ranked
    list of chunk IDs (best first). Returns IDs sorted by fused score desc.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)


# ---------- Public API ----------


async def retrieve_legal(query: str, *, persona: Persona | str = Persona.CITIZEN,
                          top_k: int | None = None) -> list[RetrievedChunk]:
    settings = get_settings()
    persona_val = persona.value if isinstance(persona, Persona) else persona
    final_k = top_k or (
        settings.practitioner_max_results if persona_val == "practitioner"
        else settings.legal_final_k if persona_val == "founder"
        else settings.citizen_max_results
    )

    chunks = await store.list_legal_chunks()
    if not chunks:
        return []

    # Dense.
    q_emb = (await embed([query]))[0]
    dense_scored: list[tuple[str, float]] = []
    for c in chunks:
        emb = c.get("embedding")
        if emb is None:
            continue
        dense_scored.append((c["id"], _cosine(q_emb, emb)))
    dense_scored.sort(key=lambda x: x[1], reverse=True)

    # Lexical.
    q_tokens = _tokenize(query)
    lex_scored: list[tuple[str, float]] = []
    for c in chunks:
        lex_scored.append((c["id"], _bm25ish(q_tokens, c["text"])))
    lex_scored.sort(key=lambda x: x[1], reverse=True)

    # Section-direct boost: if the query mentions a section number and act,
    # surface that exact section to the top.
    section_hits = _section_lookup_ids(query, chunks)

    fused = _rrf_fuse(
        [
            section_hits,
            [cid for cid, _ in dense_scored[:settings.legal_topk]],
            [cid for cid, _ in lex_scored[:settings.legal_topk]],
        ],
        k=settings.rrf_k,
    )

    cosine_by_id = dict(dense_scored)
    lexical_by_id = dict(lex_scored)

    # Filter overruled documents.
    docs = {d["id"]: d for d in await store.list_legal_documents()}
    by_id = {c["id"]: c for c in chunks}
    out: list[RetrievedChunk] = []
    for cid, score in fused:
        c = by_id.get(cid)
        if not c:
            continue
        d = docs.get(c["document_id"])
        if d and d.get("status") in ("overruled", "doubted"):
            continue
        out.append(RetrievedChunk(
            chunk_id=c["id"],
            document_id=c["document_id"],
            text=c["text"],
            chunk_type=c["chunk_type"],
            section_number=c.get("section_number"),
            hierarchy_path=c.get("hierarchy_path", []),
            score=score,
            cosine=cosine_by_id.get(cid, 0.0),
            lexical=lexical_by_id.get(cid, 0.0),
            source_kind="legal",
            metadata=c.get("metadata", {}),
        ))
        if len(out) >= final_k:
            break
    return out


async def retrieve_company(query: str, *, device_id: str,
                             top_k: int | None = None) -> list[RetrievedChunk]:
    settings = get_settings()
    final_k = top_k or settings.company_final_k
    chunks = await store.list_company_chunks(device_id)
    if not chunks:
        return []
    q_emb = (await embed([query]))[0]
    q_tokens = _tokenize(query)

    dense_scored = sorted(
        [(c["id"], _cosine(q_emb, c.get("embedding") or [])) for c in chunks],
        key=lambda x: x[1], reverse=True,
    )
    lex_scored = sorted(
        [(c["id"], _bm25ish(q_tokens, c["text"])) for c in chunks],
        key=lambda x: x[1], reverse=True,
    )
    fused = _rrf_fuse(
        [
            [cid for cid, _ in dense_scored[:settings.company_topk]],
            [cid for cid, _ in lex_scored[:settings.company_topk]],
        ],
        k=settings.rrf_k,
    )
    cosine_by_id = dict(dense_scored)
    lexical_by_id = dict(lex_scored)
    by_id = {c["id"]: c for c in chunks}
    out = []
    for cid, score in fused[:final_k]:
        c = by_id.get(cid)
        if not c:
            continue
        out.append(RetrievedChunk(
            chunk_id=c["id"],
            document_id=c["document_id"],
            text=c["text"],
            chunk_type="paragraph",
            section_number=None,
            hierarchy_path=[],
            score=score,
            cosine=cosine_by_id.get(cid, 0.0),
            lexical=lexical_by_id.get(cid, 0.0),
            source_kind="company",
            metadata=c.get("metadata", {}),
        ))
    return out


def _section_lookup_ids(query: str, chunks: list[dict]) -> list[str]:
    """If the query mentions 'Section <num> <act>', return matching chunk IDs first."""
    m = re.search(r"(?:section|s\.|sec\.?|§)\s*(\d+[A-Z]*)\s*(?:of\s+the\s+)?([A-Za-z ]+)?",
                   query, re.I)
    if not m:
        return []
    num = m.group(1).strip()
    act_hint = (m.group(2) or "").strip().lower()
    out = []
    for c in chunks:
        if c.get("section_number") != num:
            continue
        path = " ".join(c.get("hierarchy_path") or []).lower()
        if not act_hint or any(word in path for word in act_hint.split()):
            out.append(c["id"])
    return out


def support_density(retrieved: list[RetrievedChunk]) -> float:
    """Quality signal for the refusal floor.

    Calibrated against the live audit (2026-04-29):
      - Real answerable queries cluster top-1 cosine 0.34–0.69
      - Out-of-scope queries cluster 0.13–0.22
      - Borderline-but-still-answerable queries (noise nuisance, harassment,
        loan recovery) cluster 0.25–0.30 — so a single top-1 threshold lands
        right in the middle of the legitimate band.
    Fix: use the MAX of three signals so we accept if ANY says we have support:
      - top-1 cosine  (strict semantic match)
      - top-3 mean cosine  (cluster of moderate-relevance chunks)
      - top-1 lexical overlap  (exact-phrase / section-number queries)
    """
    if not retrieved:
        return 0.0
    top1_cos = retrieved[0].cosine
    top1_lex = retrieved[0].lexical
    top3 = retrieved[:3]
    top3_mean = sum(c.cosine for c in top3) / len(top3) if top3 else 0.0
    return max(top1_cos, top3_mean, top1_lex)
