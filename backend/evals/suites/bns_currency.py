"""BNS currency.

For criminal-law queries:
  - Post-1-Jul-2024 facts → BNS must appear in citations (and not only IPC).
  - Pre-1-Jul-2024 facts → IPC is acceptable / preferred.

We're lenient: if BOTH BNS and IPC are cited (helpful for clarity), that's a
pass either way. We fail only when the cited regime is wrong for the date.
"""
from __future__ import annotations

from app.agents.graph import run_agent
from evals._common import EvalResult, boot_corpus, gather_bounded, load_gold


THRESHOLD = 0.80


async def _one(entry):
    state = await run_agent(device_id="eval-bns", conversation_id=None, query=entry["query"])
    acts_cited = {c.act for c in state.citations if c.type == "section"}
    body_lower = (state.answer_md or "").lower()
    has_bns = "BNS" in acts_cited or "bns" in body_lower or "bharatiya nyaya" in body_lower
    has_ipc = "IPC" in acts_cited or "ipc" in body_lower or "indian penal code" in body_lower
    expected = entry["expect_act_first"]
    forbidden_only = entry["must_not_be_only"]
    if expected == "BNS":
        ok_act = has_bns
        wrong_only = has_ipc and not has_bns
    else:
        ok_act = has_ipc
        wrong_only = has_bns and not has_ipc
    passed = ok_act and not wrong_only
    return {
        "id": entry["id"], "passed": passed,
        "has_bns": has_bns, "has_ipc": has_ipc,
        "expected": expected, "must_not_be_only": forbidden_only,
        "confidence": state.confidence,
        "preview": state.answer_md[:240],
        "reason": ("ok" if passed else
                    f"expected={expected}, has_bns={has_bns}, has_ipc={has_ipc}"),
    }


async def run() -> EvalResult:
    await boot_corpus()
    result = EvalResult(suite="bns_currency")
    entries = list(load_gold("bns_currency"))
    rows = await gather_bounded([_one(e) for e in entries], concurrency=4)
    for r in rows:
        rid = r.pop("id"); passed = r.pop("passed")
        result.add(id=rid, passed=passed, **r)

    n = len(result.items)
    n_pass = sum(1 for i in result.items if i["passed"])
    rate = n_pass / n if n else 0
    result.finalize(
        aggregate={"n": n, "passed": n_pass, "accuracy": round(rate, 3),
                    "threshold": THRESHOLD},
        threshold_met=(rate >= THRESHOLD),
    )
    return result
