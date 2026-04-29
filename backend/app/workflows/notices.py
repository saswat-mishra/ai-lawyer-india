"""Legal notice workflows. Output is a notarisable draft notice."""
from __future__ import annotations

import json
from typing import Any

from app.llm.openai_client import ChatMessage, chat_complete
from app.rag.retriever import retrieve_legal


_NOTICE_DEFS: dict[str, dict[str, Any]] = {
    "s138_ni_act_notice": {
        "title": "Statutory Demand Notice under Section 138 NI Act",
        "required": ["payee_name", "payee_address", "drawer_name", "drawer_address",
                       "cheque_number", "cheque_date", "cheque_amount_inr", "bank_name",
                       "dishonour_date", "underlying_debt"],
        "seed_query": "Section 138 Negotiable Instruments Act statutory demand notice 30 days",
    },
    "eviction_notice": {
        "title": "Notice to Quit / Termination of Tenancy",
        "required": ["landlord_name", "tenant_name", "premises_address",
                       "ground", "notice_period_days", "state"],
        "seed_query": "Section 106 Transfer of Property Act notice to quit eviction",
    },
    "consumer_complaint_notice": {
        "title": "Consumer Complaint Notice",
        "required": ["complainant", "opposite_party", "service_or_goods",
                       "deficiency", "amount_paid_inr", "relief_sought"],
        "seed_query": "Consumer Protection Act 2019 deficiency in service unfair trade practice",
    },
    "breach_of_contract_notice": {
        "title": "Notice for Breach of Contract",
        "required": ["claimant", "respondent", "contract_date", "breach_description",
                       "cure_period_days", "damages_claimed_inr"],
        "seed_query": "Section 73 Indian Contract Act damages breach of contract",
    },
    "defamation_notice": {
        "title": "Defamation Notice",
        "required": ["claimant", "respondent", "alleged_statement", "publication_date",
                       "harm_description", "relief_sought"],
        "seed_query": "BNS Section 356 IPC Section 499 500 defamation notice",
    },
}


def title_for(workflow: str, inputs: dict[str, Any]) -> str:
    base = _NOTICE_DEFS.get(workflow, {}).get("title", workflow.replace("_", " ").title())
    name_hint = inputs.get("payee_name") or inputs.get("claimant") or ""
    return f"{base}{(' — ' + name_hint) if name_hint else ''}"


async def generate(workflow: str, inputs: dict[str, Any], *,
                    device_id: str) -> tuple[str, list[dict[str, Any]]]:
    spec = _NOTICE_DEFS.get(workflow)
    if not spec:
        raise ValueError(f"unknown notice workflow {workflow}")
    missing = [k for k in spec["required"] if not inputs.get(k)]
    if missing:
        raise ValueError(f"missing required inputs: {', '.join(missing)}")

    retrieved = await retrieve_legal(spec["seed_query"], top_k=6)
    legal_block = "\n\n".join(
        f"[L{i+1}] {' > '.join(c.hierarchy_path)}\n{c.text[:900]}"
        for i, c in enumerate(retrieved)
    ) or "(no retrievals)"

    sys = ChatMessage("system",
        "You are a senior Indian advocate drafting a formal legal notice. "
        "Use the standard structure: heading, parties, facts, statutory basis, demand, "
        "consequence on non-compliance, signature block. Cite Indian Acts and Sections only. "
        "Never invent citations. End with a fenced JSON citation trailer.")
    user = ChatMessage("user",
        f"Notice type: {spec['title']}\n"
        f"Inputs: {json.dumps(inputs, ensure_ascii=False)}\n\n"
        f"AUTHORITATIVE RETRIEVAL:\n{legal_block}\n\n"
        f"Draft the notice. After the body, append a fenced ```json{{\"citations\": [...]}}``` block.")
    text = await chat_complete([sys, user], temperature=0.2, max_tokens=1800)
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
