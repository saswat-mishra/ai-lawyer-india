"""OpenAI client wrapper with deterministic mock fallback.

Design: every LLM call goes through `chat_complete`, `chat_stream`, or `embed`.
When OPENAI_API_KEY is unset, requests are served by a deterministic mock.
This is what lets the full test suite run before the user adds the key.

The mock is *not* a stub — it produces structured outputs that match the schema
real models would return, so the rest of the pipeline (parser, verifier, agent)
can be exercised end-to-end.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
from dataclasses import dataclass
from typing import Any, AsyncIterator

from app.core.config import get_settings


@dataclass
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


# ---------------- Public surface ----------------


async def chat_complete(messages: list[ChatMessage], *, model: str | None = None,
                         temperature: float = 0.2, response_format: str | None = None,
                         max_tokens: int = 1500) -> str:
    settings = get_settings()
    if not settings.has_openai:
        return _mock_chat_complete(messages, response_format)
    return await _real_chat_complete(messages, model=model or settings.openai_model_default,
                                       temperature=temperature,
                                       response_format=response_format,
                                       max_tokens=max_tokens)


async def chat_stream(messages: list[ChatMessage], *, model: str | None = None,
                       temperature: float = 0.2, max_tokens: int = 1500
                       ) -> AsyncIterator[str]:
    settings = get_settings()
    if not settings.has_openai:
        async for tok in _mock_chat_stream(messages):
            yield tok
        return
    async for tok in _real_chat_stream(messages, model=model or settings.openai_model_default,
                                          temperature=temperature, max_tokens=max_tokens):
        yield tok


async def embed(texts: list[str], *, model: str | None = None,
                  input_type: str = "document") -> list[list[float]]:
    """Embed batch — routes to Voyage AI when EMBEDDING_BACKEND=voyage,
    otherwise OpenAI, otherwise the deterministic mock."""
    settings = get_settings()
    # Phase 2 activation: Voyage law-2 (legal-tuned).
    try:
        from app.llm import voyage_client
        if voyage_client.is_enabled():
            return await voyage_client.embed(texts, input_type=input_type)
    except Exception:
        pass  # fall through to OpenAI / mock
    if not settings.has_openai:
        return [_mock_embed(t, settings.openai_embedding_dim) for t in texts]
    return await _real_embed(texts, model=model or settings.openai_embedding_model,
                                dim=settings.openai_embedding_dim)


# ---------------- Real implementations ----------------


def _client():
    from openai import AsyncOpenAI
    return AsyncOpenAI(api_key=get_settings().openai_api_key)


async def _real_chat_complete(messages: list[ChatMessage], *, model: str,
                                temperature: float, response_format: str | None,
                                max_tokens: int) -> str:
    client = _client()
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [m.to_dict() for m in messages],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format == "json":
        kwargs["response_format"] = {"type": "json_object"}
    resp = await client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""


async def _real_chat_stream(messages: list[ChatMessage], *, model: str,
                              temperature: float, max_tokens: int
                              ) -> AsyncIterator[str]:
    client = _client()
    stream = await client.chat.completions.create(
        model=model,
        messages=[m.to_dict() for m in messages],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta


async def _real_embed(texts: list[str], *, model: str, dim: int) -> list[list[float]]:
    client = _client()
    resp = await client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]


# ---------------- Mock implementations ----------------
# Deterministic, schema-aware. Designed so the rest of the pipeline can be
# tested without a network call.

# A fact pattern -> canned answer used in non-OpenAI tests. Falls through to
# a generic citation-bearing template if no pattern matches.
_PATTERNS: list[tuple[re.Pattern, dict[str, Any]]] = [
    (re.compile(r"murder|section\s*302|killed|stabbed", re.I), {
        "short_answer": "Murder is now prosecuted under Section 103 BNS (formerly Section 302 IPC).",
        "citations": [
            {"type": "section", "act": "BNS", "section": "103", "para": None},
            {"type": "section", "act": "IPC", "section": "302", "para": None},
        ],
        "confidence": "high",
    }),
    (re.compile(r"cheque\s*bounce|\bs(?:ection)?\.?\s*138\b|negotiable\s*instruments|\bni\s*act\b", re.I), {
        "short_answer": "Section 138 of the Negotiable Instruments Act, 1881 governs cheque dishonour.",
        "citations": [
            {"type": "section", "act": "NI Act", "section": "138", "para": None},
        ],
        "confidence": "high",
    }),
    (re.compile(r"landlord|evict|tenant|rent", re.I), {
        "short_answer": "Eviction grounds and notice requirements depend on the governing rent control statute and contract.",
        "citations": [
            {"type": "section", "act": "Maharashtra Rent Control Act", "section": "16", "para": None},
            {"type": "section", "act": "Transfer of Property Act", "section": "106", "para": None},
        ],
        "confidence": "medium",
        "needs_clarification": ["state", "tenancy_type"],
    }),
    (re.compile(r"defamation|defame", re.I), {
        "short_answer": "Defamation is now under Sections 356(1) and 356(2) BNS (formerly Sections 499 and 500 IPC).",
        "citations": [
            {"type": "section", "act": "BNS", "section": "356", "para": None},
        ],
        "confidence": "high",
    }),
]


def _mock_chat_complete(messages: list[ChatMessage], response_format: str | None) -> str:
    user_text = next((m.content for m in reversed(messages) if m.role == "user"), "")
    system_text = "\n".join(m.content for m in messages if m.role == "system")
    if "classify" in system_text.lower():
        return _mock_classify(user_text)
    if "clarify" in system_text.lower() or "missing information" in system_text.lower():
        return _mock_clarify(user_text, response_format)
    if "verify" in system_text.lower() and "citation" in system_text.lower():
        return _mock_verify(user_text, response_format)
    if response_format == "json":
        return json.dumps(_mock_payload(user_text))
    return _mock_prose(user_text)


async def _mock_chat_stream(messages: list[ChatMessage]) -> AsyncIterator[str]:
    full = _mock_chat_complete(messages, None)
    # Stream in 10-character chunks for realism.
    for i in range(0, len(full), 10):
        await asyncio.sleep(0.005)
        yield full[i:i + 10]


def _mock_payload(query: str) -> dict[str, Any]:
    for pat, payload in _PATTERNS:
        if pat.search(query):
            return payload
    return {
        "short_answer": "I couldn't find authoritative basis for this question in my corpus. Please consult an advocate specialising in this area.",
        "citations": [],
        "confidence": "refused",
    }


def _mock_prose(query: str) -> str:
    payload = _mock_payload(query)
    cites = payload.get("citations", [])
    cite_str = ", ".join(f"[{c.get('act')} §{c.get('section')}]" for c in cites)
    return f"{payload['short_answer']} {cite_str}".strip()


def _mock_classify(text: str) -> str:
    """Return JSON {category, jurisdiction_hint, slots_needed}."""
    cat = "general"
    if re.search(r"murder|robbery|theft|assault|rape", text, re.I):
        cat = "criminal"
    elif re.search(r"contract|nda|agreement|breach", text, re.I):
        cat = "contract"
    elif re.search(r"landlord|tenant|property|sale\s*deed", text, re.I):
        cat = "property"
    elif re.search(r"divorce|custody|maintenance|marriage", text, re.I):
        cat = "family"
    elif re.search(r"company|director|sebi|rbi|gst", text, re.I):
        cat = "corporate"
    return json.dumps({"category": cat, "jurisdiction_hint": None, "slots_needed": []})


def _mock_clarify(text: str, response_format: str | None) -> str:
    questions: list[dict[str, Any]] = []
    if re.search(r"landlord|tenant|evict|rent", text, re.I):
        questions = [
            {"slot": "state", "question": "Which state is the property in?",
             "choices": ["Maharashtra", "Delhi", "Karnataka", "Other"]},
            {"slot": "tenancy_type", "question": "Is the agreement a registered tenancy or a leave-and-licence?",
             "choices": ["Registered tenancy", "Leave-and-licence", "Unregistered/oral", "Not sure"]},
        ]
    elif re.search(r"company|founder|startup|board", text, re.I):
        questions = [
            {"slot": "company_form", "question": "What is the entity type?",
             "choices": ["Private Limited", "LLP", "OPC", "Partnership", "Sole Prop"]},
        ]
    elif re.search(r"crime|fir|arrest|police", text, re.I):
        questions = [
            {"slot": "incident_state", "question": "Which state did the incident occur in?",
             "choices": ["Maharashtra", "Delhi", "Karnataka", "Uttar Pradesh", "Other"]},
            {"slot": "incident_date", "question": "When did the incident occur (BNS applies on/after 1 Jul 2024)?",
             "choices": ["Before 1 Jul 2024", "On/after 1 Jul 2024", "Unsure"]},
        ]
    return json.dumps({"questions": questions})


def _mock_verify(text: str, response_format: str | None) -> str:
    """Return entailment label for a (claim, evidence) pair embedded in text."""
    return json.dumps({"label": "entails" if "entails" in text or "consistent" in text else "not_supported"})


def _mock_embed(text: str, dim: int) -> list[float]:
    """Deterministic pseudo-embedding from SHA-256. Same text -> same vector.
    Cosine similarity between similar phrases is *not* meaningful here, but the
    distribution and shape are correct, which is what the pipeline needs.
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Cycle bytes to produce `dim` floats in [-1, 1].
    out: list[float] = []
    while len(out) < dim:
        for b in h:
            out.append((b - 128) / 128.0)
            if len(out) >= dim:
                break
        h = hashlib.sha256(h).digest()
    # Normalise to unit vector for cosine.
    norm = sum(x * x for x in out) ** 0.5 or 1.0
    return [x / norm for x in out]
