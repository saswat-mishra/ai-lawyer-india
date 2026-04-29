"""Persona differentiation.

Same query under Citizen vs Practitioner. Outputs must differ materially:
- Practitioner output is at least 1.3x as long, OR
- Practitioner uses substantially more legal jargon (Latin terms, section refs).

This is a quality signal, not a hard correctness gate.
"""
from __future__ import annotations

import re

from app.agents.graph import run_agent
from app.core.config import Persona
from app.db import store
from evals._common import EvalResult, boot_corpus, gather_bounded, load_gold


JARGON_TERMS = (
    "section ", "sub-section", "ratio", "obiter", "limitation",
    "bona fide", "mens rea", "actus reus", "prima facie", "vide", "ergo",
    "ipso facto", "in pari materia", "ex parte", "sub silentio",
    "judgment", "appellant", "respondent", "petitioner", "plaintiff",
    "defendant", "decree", "ratio decidendi", "constitutional bench",
    "high court", "supreme court", "interlocutory", "writ",
)


def _jargon_score(text: str) -> int:
    t = text.lower()
    return sum(t.count(term) for term in JARGON_TERMS)


THRESHOLD = 0.66  # 2/3 of paired-comparisons must show differentiation


async def _one(entry):
    await store.upsert_device("eval-cit", persona="citizen")
    cit = await run_agent(device_id="eval-cit", conversation_id=None, query=entry["query"])
    await store.upsert_device("eval-prac", persona="practitioner")
    prac = await run_agent(device_id="eval-prac", conversation_id=None, query=entry["query"])
    len_ratio = (len(prac.answer_md) / len(cit.answer_md)) if cit.answer_md else 0
    jargon_ratio = _jargon_score(prac.answer_md) / max(1, _jargon_score(cit.answer_md))
    differentiated = (len_ratio >= 1.3) or (jargon_ratio >= 1.5)
    return {
        "id": entry["id"], "passed": differentiated,
        "len_citizen": len(cit.answer_md), "len_practitioner": len(prac.answer_md),
        "len_ratio": round(len_ratio, 2),
        "jargon_citizen": _jargon_score(cit.answer_md),
        "jargon_practitioner": _jargon_score(prac.answer_md),
        "jargon_ratio": round(jargon_ratio, 2),
        "reason": ("differentiated" if differentiated
                    else f"len_ratio={len_ratio:.2f}, jargon_ratio={jargon_ratio:.2f}"),
    }


async def run() -> EvalResult:
    await boot_corpus()
    result = EvalResult(suite="persona")
    entries = list(load_gold("persona"))
    rows = await gather_bounded([_one(e) for e in entries], concurrency=2)
    for r in rows:
        rid = r.pop("id"); passed = r.pop("passed")
        result.add(id=rid, passed=passed, **r)

    n = len(result.items)
    n_pass = sum(1 for i in result.items if i["passed"])
    rate = n_pass / n if n else 0
    result.finalize(
        aggregate={"n": n, "passed": n_pass, "rate": round(rate, 3),
                    "threshold": THRESHOLD},
        threshold_met=(rate >= THRESHOLD),
    )
    return result
