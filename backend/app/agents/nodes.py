"""Agent nodes. Each is an async function: AgentState -> AgentState.

Pipeline:
    classify -> clarify -> retrieve -> synthesize -> verify -> finalize

The graph is linear by default. clarify can short-circuit when slots are missing,
returning the state with `needs_clarification=True` so the API hands the
clarifying questions to the user before proceeding.
"""
from __future__ import annotations

import asyncio
import json
import re
from typing import Any

from app.agents.state import AgentState
from app.core.config import Persona, get_settings
from app.db import store
from app.llm.openai_client import ChatMessage, chat_complete
from app.rag.retriever import retrieve_company, retrieve_legal, support_density
from app.verify.citations import Citation, parse_citations, strip_unverified, verify_citations


# ---------- Prompt fragments ----------

_PERSONA_BLURB = {
    "citizen": (
        "Reader is a non-lawyer Indian citizen. Use plain English. Avoid jargon. "
        "Lead with the practical answer. Keep paragraphs short. End with a 'next steps' list."
    ),
    "founder": (
        "Reader is a founder/CEO of an Indian company. Be concise and decisive. "
        "Highlight commercial impact, regulatory risk, and what to ask their lawyer. "
        "When relevant, leverage the company's own documents (clearly labelled)."
    ),
    "practitioner": (
        "Reader is a lawyer/advocate in India. Use precise legal register. "
        "Cite Section + Act and primary cases. Provide ratio and procedural posture. "
        "Surface counter-arguments and limitation."
    ),
}

_BNS_NOTE = (
    "Note temporal regime: for criminal offences on/after 1 July 2024, use BNS/BNSS/BSA. "
    "For prior offences, IPC/CrPC/Evidence Act apply. If date is unclear, ask."
)

_REFUSAL_BODY = (
    "I couldn't find authoritative basis for this question in my corpus. "
    "This is likely because the matter is highly fact-specific, requires state-level "
    "rules I don't have indexed, or is outside scope. "
    "Recommended next step: consult an enrolled advocate practising in this area."
)


# ---------- Nodes ----------


async def classify(state: AgentState) -> AgentState:
    sys = ChatMessage("system",
        "You classify Indian legal queries. Output JSON only. Be conservative "
        "about slots_needed — only list a slot if the ANSWER WOULD MATERIALLY "
        "CHANGE based on it. Informational/definitional questions ('what is X', "
        "'explain Y', 'compare A and B') should have slots_needed=[]. Only list "
        "slots when the user describes a specific dispute, event, or fact pattern "
        "where jurisdiction, dates, parties, or amounts decide the outcome.")
    user = ChatMessage("user",
        f"Categories: criminal, civil, contract, property, family, corporate, "
        f"tax, ip, labour, consumer, constitutional, general.\n\n"
        f"Query: {state.user_query}\n\n"
        f"Respond JSON: {{\"category\": str, \"slots_needed\": [str], "
        f"\"is_factspecific\": bool}}. "
        f"slots_needed must be [] when is_factspecific is false.")
    raw = await chat_complete([sys, user], response_format="json", temperature=0.0,
                                max_tokens=200)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"category": "general", "slots_needed": [], "is_factspecific": False}
    state.category = data.get("category", "general")
    needed = data.get("slots_needed", []) if data.get("is_factspecific", False) else []
    state.slots.setdefault("_needed", needed)
    state.log("classify", category=state.category,
                is_factspecific=data.get("is_factspecific", False),
                slots_needed=needed)
    return state


_DATE_RE = re.compile(
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+\d{4}\b"
    r"|\b\d{4}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}/\d{1,2}/\d{4}\b",
    re.I,
)
_INDIAN_STATES_RE = re.compile(
    r"\b(?:Maharashtra|Mumbai|Pune|Delhi|Karnataka|Bengaluru|Bangalore|"
    r"Tamil\s*Nadu|Chennai|West\s*Bengal|Kolkata|Uttar\s*Pradesh|Lucknow|"
    r"Rajasthan|Jaipur|Gujarat|Ahmedabad|Punjab|Haryana|Bihar|Patna|"
    r"Telangana|Hyderabad|Andhra\s*Pradesh|Kerala|Odisha|Madhya\s*Pradesh|"
    r"Jharkhand|Chhattisgarh|Assam|Goa|Himachal\s*Pradesh|Uttarakhand|"
    r"Tripura|Meghalaya|Manipur|Nagaland|Mizoram|Sikkim|Arunachal\s*Pradesh)\b",
    re.I,
)


def _slot_evident_in_query(slot: str, query: str) -> bool:
    """Heuristic: skip slots whose value is clearly already in the query."""
    s = slot.lower()
    q = query
    if "date" in s or "time" in s or "when" in s:
        return bool(_DATE_RE.search(q))
    if "state" in s or "jurisdiction" in s or "location" in s or "place" in s:
        return bool(_INDIAN_STATES_RE.search(q))
    return False


async def clarify(state: AgentState) -> AgentState:
    """Decide whether we need to ask the user for clarification."""
    needed = state.slots.get("_needed") or []
    given = {k.lower() for k in state.slots.keys()}
    needed = [
        s for s in needed
        if s.lower() not in given
        and not _slot_evident_in_query(s, state.user_query)
    ][:3]
    if not needed:
        state.log("clarify", asked=False)
        return state

    sys = ChatMessage("system",
        "You generate 1-3 high-leverage clarifying questions for an Indian legal query. "
        "Each question must have multiple-choice options PLUS a free-text fallback. "
        "Output JSON only.")
    user = ChatMessage("user",
        f"Query: {state.user_query}\nMissing slots: {needed}\n\n"
        f"Respond JSON: {{\"questions\": [{{\"slot\": str, \"question\": str, "
        f"\"choices\": [str], \"allow_free_text\": true}}]}}.")
    raw = await chat_complete([sys, user], response_format="json", temperature=0.1,
                                max_tokens=400)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"questions": []}
    qs = data.get("questions", [])[:3]
    state.clarifying_questions = qs
    state.needs_clarification = bool(qs)
    state.log("clarify", asked=bool(qs), count=len(qs))
    return state


async def retrieve(state: AgentState) -> AgentState:
    legal_task = retrieve_legal(state.user_query, persona=state.persona)
    company_task = retrieve_company(state.user_query, device_id=state.device_id)
    legal, company = await asyncio.gather(legal_task, company_task)
    state.legal_results = legal
    state.company_results = company
    state.support_density = support_density(legal)
    state.log("retrieve",
                legal_count=len(legal), company_count=len(company),
                support=state.support_density)
    return state


async def synthesize(state: AgentState) -> AgentState:
    settings = get_settings()
    if state.support_density < settings.refusal_floor and not state.company_results:
        state.refused = True
        state.refusal_reason = "low_support"
        state.confidence = "refused"
        state.answer_md = _REFUSAL_BODY
        state.log("synthesize", refused=True)
        return state

    persona_val = state.persona.value if isinstance(state.persona, Persona) else state.persona
    persona_blurb = _PERSONA_BLURB.get(persona_val, _PERSONA_BLURB["citizen"])

    legal_blocks = _format_blocks(state.legal_results, kind="legal")
    company_blocks = _format_blocks(state.company_results, kind="company")

    sys = ChatMessage("system", _build_system_prompt(persona_blurb))
    user = ChatMessage("user",
        f"USER QUESTION:\n{state.user_query}\n\n"
        f"AUTHORITATIVE SOURCES (Indian law):\n{legal_blocks or '(none)'}\n\n"
        f"COMPANY-PROVIDED CONTEXT (the user's own documents):\n{company_blocks or '(none)'}\n\n"
        f"INSTRUCTIONS:\n"
        f"- Use ONLY the sources above; do not introduce outside citations.\n"
        f"- Cite using [SECT:Act:Number] for sections and [CASE:short_citation] for cases.\n"
        f"- For company sources cite [COMPANY:doc_name].\n"
        f"- If a source contradicts your draft answer, prefer the source.\n"
        f"- {_BNS_NOTE}\n"
        f"- End with a JSON block fenced as ```json{{...}}``` containing structured "
        f"citations and a confidence label (high/medium/low).")
    md = await chat_complete([sys, user], temperature=0.2, max_tokens=1400)

    # Extract structured trailer.
    body, structured = _split_structured_trailer(md)
    state.answer_md = body
    cites = parse_citations(body)
    cites += _structured_to_citations(structured)
    state.citations = cites
    state.confidence = (structured.get("confidence")
                          if isinstance(structured, dict) else None) or "medium"
    state.log("synthesize", citations=len(cites), confidence=state.confidence)
    return state


async def verify(state: AgentState) -> AgentState:
    if state.refused:
        return state
    evidence_chunks = [{"text": c.text} for c in state.legal_results + state.company_results]
    result = await verify_citations(state.citations, evidence_chunks=evidence_chunks)
    if not result.faithful:
        # Strip raw unverified citations from the body.
        state.answer_md = strip_unverified(state.answer_md, result)
    state.citations = result.verified
    state.log("verify",
                verified=len(result.verified),
                unverified=len(result.unverified),
                quote_failures=len(result.quote_failures))
    if result.unverified or result.quote_failures:
        # Downgrade confidence if any citations were stripped.
        if state.confidence == "high":
            state.confidence = "medium"
        elif state.confidence == "medium":
            state.confidence = "low"
    return state


async def finalize(state: AgentState) -> AgentState:
    """Persist message + audit trail."""
    if not state.conversation_id:
        return state
    await store.add_message(
        state.conversation_id,
        role="assistant",
        content=state.answer_md,
        meta={
            "citations": [c.to_dict() for c in state.citations],
            "trace": state.trace,
            "category": state.category,
            "support_density": state.support_density,
        },
        confidence=state.confidence,
    )
    await store.audit("synthesis",
                        device_id=state.device_id,
                        conversation_id=state.conversation_id,
                        payload={
                            "category": state.category,
                            "confidence": state.confidence,
                            "trace": state.trace,
                        })
    return state


# ---------- Helpers ----------


def _build_system_prompt(persona_blurb: str) -> str:
    return (
        "You are an India-first AI lawyer answering on the basis of cited Indian law. "
        f"{persona_blurb}\n\n"
        "Strict rules:\n"
        "- Never invent citations. Use only sources provided.\n"
        "- If a question can't be answered from provided sources, say so.\n"
        "- Distinguish company-provided context from public Indian law.\n"
        "- Be honest about uncertainty.\n"
    )


def _format_blocks(chunks, *, kind: str) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        path = " > ".join(c.hierarchy_path) if c.hierarchy_path else ""
        header = f"[{kind.upper()} {i}] {path}".strip()
        if c.section_number:
            header += f" §{c.section_number}"
        snippet = (c.text[:1200] + "...") if len(c.text) > 1200 else c.text
        parts.append(f"{header}\n{snippet}")
    return "\n\n".join(parts)


_TRAILER_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S | re.I)


def _split_structured_trailer(md: str) -> tuple[str, dict]:
    m = _TRAILER_RE.search(md)
    if not m:
        return md, {}
    body = (md[:m.start()] + md[m.end():]).strip()
    try:
        return body, json.loads(m.group(1))
    except json.JSONDecodeError:
        return body, {}


def _structured_to_citations(payload: dict) -> list[Citation]:
    out: list[Citation] = []
    for c in (payload.get("citations") or []):
        if c.get("type") == "section":
            out.append(Citation(type="section", raw=str(c),
                                  act=c.get("act"), section=c.get("section")))
        elif c.get("type") == "case":
            out.append(Citation(type="case", raw=str(c),
                                  case_name=c.get("case_name"),
                                  citation_str=c.get("citation_str")))
    return out
