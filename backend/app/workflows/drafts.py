"""Draft workflows.

Each workflow has:
- Required inputs schema (declared, validated).
- A retrieval seed query (so RAG pulls the controlling sections + cases).
- A template that the LLM fills in, with a strict citation policy.

State-aware fields (governing law, stamp duty, registration) are surfaced as
inputs the user must fill, not invented. We deliberately do NOT pretend to
know exact stamp duty rates — we ask the user / state-specific module.
"""
from __future__ import annotations

import json
from typing import Any

from app.llm.openai_client import ChatMessage, chat_complete
from app.rag.retriever import retrieve_legal


_WORKFLOW_DEFS: dict[str, dict[str, Any]] = {
    "rental_agreement": {
        "title": "Rental / Leave-and-Licence Agreement",
        "required": ["state", "landlord_name", "tenant_name", "premises_address",
                       "monthly_rent_inr", "deposit_inr", "tenure_months", "start_date"],
        "seed_query": "leave and licence agreement essential clauses Transfer of Property Act stamp duty registration",
    },
    "nda": {
        "title": "Mutual Non-Disclosure Agreement",
        "required": ["disclosing_party", "receiving_party", "purpose",
                       "duration_months", "governing_law_state"],
        "seed_query": "non-disclosure agreement India confidentiality Section 27 Indian Contract Act",
    },
    "employment_letter": {
        "title": "Offer / Appointment Letter",
        "required": ["company_name", "candidate_name", "role", "ctc_inr",
                       "start_date", "city", "probation_months"],
        "seed_query": "employment offer letter India Industrial Employment Standing Orders POSH Act gratuity",
    },
    "founders_agreement": {
        "title": "Founders' Agreement",
        "required": ["founders", "company_name", "equity_split", "vesting_schedule",
                       "ip_assignment", "governing_law_state"],
        "seed_query": "founders agreement India vesting cliff IP assignment Companies Act",
    },
    "vendor_msa": {
        "title": "Master Services Agreement",
        "required": ["customer", "vendor", "scope", "fees_terms",
                       "governing_law_state", "indemnity_cap"],
        "seed_query": "master services agreement India indemnity limitation of liability DPDP Act",
    },
    "consultancy_agreement": {
        "title": "Consultancy Agreement",
        "required": ["principal", "consultant", "scope", "fees", "duration_months"],
        "seed_query": "consultancy agreement India principal-consultant Section 194J TDS",
    },
    "partnership_deed": {
        "title": "Partnership Deed",
        "required": ["partners", "firm_name", "capital_contribution", "profit_share",
                       "place_of_business"],
        "seed_query": "Indian Partnership Act 1932 partnership deed essentials",
    },
    "will": {
        "title": "Will (Indian Succession Act)",
        "required": ["testator_name", "religion", "beneficiaries", "executor",
                       "assets_summary"],
        "seed_query": "Indian Succession Act will registration attestation Section 63",
    },
}


def title_for(workflow: str, inputs: dict[str, Any]) -> str:
    base = _WORKFLOW_DEFS.get(workflow, {}).get("title", workflow.replace("_", " ").title())
    name_hint = inputs.get("company_name") or inputs.get("candidate_name") or \
                  inputs.get("tenant_name") or inputs.get("firm_name") or ""
    return f"{base}{(' — ' + name_hint) if name_hint else ''}"


async def generate(workflow: str, inputs: dict[str, Any], *,
                    device_id: str) -> tuple[str, list[dict[str, Any]]]:
    spec = _WORKFLOW_DEFS.get(workflow)
    if not spec:
        raise ValueError(f"unknown workflow {workflow}")
    missing = [k for k in spec["required"] if not inputs.get(k)]
    if missing:
        raise ValueError(f"missing required inputs: {', '.join(missing)}")

    retrieved = await retrieve_legal(spec["seed_query"], top_k=8)
    legal_block = "\n\n".join(
        f"[L{i+1}] {' > '.join(c.hierarchy_path)}\n{c.text[:1000]}"
        for i, c in enumerate(retrieved)
    ) or "(no retrievals — generic best-practice template)"

    sys = ChatMessage("system",
        "You are an expert Indian transactional lawyer. Draft a clean, "
        "production-quality agreement in clear legal English. "
        "Use only Indian legal references (Sections + Acts). Do not invent citations. "
        "Output Markdown with numbered clauses. End with a structured JSON trailer of citations.")
    user = ChatMessage("user",
        f"Workflow: {spec['title']}\n"
        f"Inputs: {json.dumps(inputs, ensure_ascii=False)}\n\n"
        f"AUTHORITATIVE RETRIEVAL:\n{legal_block}\n\n"
        f"Draft the document. Embed inline citations like [SECT:Act:Number]. "
        f"After the draft, append a fenced ```json{{\"citations\": [{{...}}]}}``` block.")
    text = await chat_complete([sys, user], temperature=0.2, max_tokens=2200)

    body, citations = _split_json(text)
    return body, citations


def _split_json(text: str) -> tuple[str, list[dict[str, Any]]]:
    import re
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S | re.I)
    if not m:
        return text, []
    body = (text[:m.start()] + text[m.end():]).strip()
    try:
        return body, json.loads(m.group(1)).get("citations", [])
    except json.JSONDecodeError:
        return body, []
