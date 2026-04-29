"""Refusal correctness.

Answerable queries should NOT refuse; out-of-scope ones SHOULD refuse (or
explicitly say "I don't know" / "consult a lawyer").
"""
from __future__ import annotations

from app.agents.graph import run_agent
from evals._common import EvalResult, boot_corpus, gather_bounded, load_gold


THRESHOLD = 0.90


def _is_refusal(state) -> bool:
    if state.refused:
        return True
    if state.confidence == "refused":
        return True
    if state.needs_clarification:
        # Asking for more info instead of fabricating IS the right behavior on
        # under-specified factual questions.
        return True
    text = (state.answer_md or "").lower()
    triggers = (
        "couldn't find authoritative basis",
        "i don't know",
        "i do not know",
        "out of scope",
        "consult an enrolled advocate",
        "i'm not able to",
        "cannot answer",
        "does not exist",
        "doesn't exist",
        "no such",
        "i cannot find",
        "cannot find",
        "no information",
        "cannot provide",
        "fabricated",
        "fictitious",
    )
    return any(t in text for t in triggers)


async def _one(entry):
    state = await run_agent(device_id="eval-rf", conversation_id=None, query=entry["query"])
    is_refused = _is_refusal(state)
    passed = is_refused == entry["should_refuse"]
    return {
        "id": entry["id"], "passed": passed,
        "should_refuse": entry["should_refuse"], "refused": is_refused,
        "confidence": state.confidence, "preview": state.answer_md[:200],
        "reason": ("ok" if passed
                    else f"expected_refusal={entry['should_refuse']}, got={is_refused}"),
    }


async def run() -> EvalResult:
    await boot_corpus()
    result = EvalResult(suite="refusal")
    entries = list(load_gold("refusal"))
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
