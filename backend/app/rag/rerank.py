"""LLM-as-reranker.

Vercel serverless functions can't fit a sentence-transformers cross-encoder
(too large vs the 250 MB function-bundle cap). Instead we use the cheapest
LLM tier (gpt-4o-mini) in a tightly-constrained structured-output mode:

    in:  query, candidates [{id, headline, snippet}]
    out: top-k candidate ids, ordered by relevance

This is "LLM-as-reranker" — a published technique used by Anthropic / OpenAI
demos and the LlamaIndex / LangChain ecosystems. It costs ~$0.005 per query
on top-50 candidates with gpt-4o-mini and adds ~1-1.5 s latency. Tradeoff is
worth it: published recall@5 lifts of 5-15 points over RRF-only retrieval on
domain corpora.

OFF by default in tests (no API key path). Enable in prod with
RERANK_ENABLED=1; controllable via the agent state.
"""
from __future__ import annotations

import json
import os
from typing import Any

from app.llm.openai_client import ChatMessage, chat_complete
from app.rag.retriever import RetrievedChunk


def is_enabled() -> bool:
    """Reranker on if explicitly enabled and we have a real OpenAI key."""
    if os.environ.get("RERANK_ENABLED") not in ("1", "true", "yes"):
        return False
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


async def rerank(query: str, candidates: list[RetrievedChunk], *,
                   top_k: int = 8, model: str | None = None
                   ) -> list[RetrievedChunk]:
    """Re-order `candidates` by relevance to `query`. Returns at most `top_k`.

    Falls through to the original ordering if the LLM call fails or returns
    malformed output — never blocks an answer on rerank quality.
    """
    if not candidates:
        return candidates
    if len(candidates) <= top_k:
        return candidates  # no point reranking

    # Build a compact view of each candidate so the prompt fits.
    items = []
    for i, c in enumerate(candidates):
        path = " > ".join(c.hierarchy_path) if c.hierarchy_path else ""
        head = path
        if c.section_number:
            head = f"{head} · §{c.section_number}".strip(" ·")
        snippet = (c.text[:280] + "…") if len(c.text) > 280 else c.text
        items.append({"id": i, "head": head, "snippet": snippet})

    sys = ChatMessage("system",
        "You rerank legal-document candidates for a user question. "
        "Score on direct relevance to the question, not general topic match. "
        "Output JSON only.")
    user = ChatMessage("user",
        f"QUESTION:\n{query}\n\n"
        f"CANDIDATES (id, head, snippet):\n{json.dumps(items, ensure_ascii=False)}\n\n"
        f"Return JSON: {{\"ranked\": [<id>, ...]}}, the FIRST {top_k} ids "
        f"being the most relevant, in descending order of relevance. "
        f"Include only ids from the list above; no explanations.")
    try:
        raw = await chat_complete(
            [sys, user],
            model=model or "gpt-4o-mini",
            response_format="json",
            temperature=0.0,
            max_tokens=400,
        )
        data = json.loads(raw)
        ranked_ids = data.get("ranked") or []
        # De-dupe and clip to top_k.
        seen: set[int] = set()
        ordered: list[RetrievedChunk] = []
        for cid in ranked_ids:
            if not isinstance(cid, int) or cid in seen or cid < 0 or cid >= len(candidates):
                continue
            seen.add(cid)
            ordered.append(candidates[cid])
            if len(ordered) >= top_k:
                break
        # Anything the LLM forgot — keep behind in the original order so we
        # never strictly *lose* a candidate.
        for i, c in enumerate(candidates):
            if i not in seen and len(ordered) < top_k:
                ordered.append(c)
        return ordered
    except Exception:
        # Hard fallback: original ordering.
        return candidates[:top_k]
