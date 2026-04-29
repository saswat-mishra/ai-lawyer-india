"""Citation faithfulness suite.

For each gold query:
  1. Run the agent end-to-end with real OpenAI.
  2. Assert: at least one expected (act, section) appears in the verified citations.
  3. Assert: no UNVERIFIED citations leaked into the final answer body.
"""
from __future__ import annotations

from app.agents.graph import run_agent
from app.verify.citations import parse_citations, verify_citations
from evals._common import EvalResult, boot_corpus, gather_bounded, load_gold


THRESHOLD = 1.0  # 100% — we ship this guarantee


async def _one(entry):
    state = await run_agent(device_id="eval-cf", conversation_id=None,
                              query=entry["query"])
    verified_pairs = {(c.act, c.section) for c in state.citations
                        if c.type == "section"}
    expected = {(e["act"], e["section"]) for e in entry.get("must_cite_any", [])}
    hit_expected = bool(verified_pairs & expected)

    body_cites = parse_citations(state.answer_md)
    body_verify = await verify_citations(body_cites)
    leaked = len(body_verify.unverified) + len(body_verify.quote_failures)

    passed = hit_expected and leaked == 0
    return {
        "id": entry["id"],
        "passed": passed,
        "verified_count": len(state.citations),
        "verified_pairs": list(verified_pairs),
        "leaked_unverified": leaked,
        "hit_expected": hit_expected,
        "confidence": state.confidence,
        "answer_preview": state.answer_md[:240],
        "reason": ("ok" if passed else
                    f"hit_expected={hit_expected} leaked={leaked} pairs={list(verified_pairs)}"),
    }


async def run() -> EvalResult:
    await boot_corpus()
    result = EvalResult(suite="citation_faithfulness")
    entries = list(load_gold("citation_faithfulness"))
    rows = await gather_bounded([_one(e) for e in entries], concurrency=4)
    for r in rows:
        passed = r.pop("passed")
        rid = r.pop("id")
        result.add(id=rid, passed=passed, **r)

    n = len(result.items)
    n_pass = sum(1 for i in result.items if i["passed"])
    pass_rate = n_pass / n if n else 0.0
    leaked_total = sum(i.get("leaked_unverified", 0) for i in result.items)
    result.finalize(
        aggregate={
            "n": n, "passed": n_pass, "pass_rate": round(pass_rate, 3),
            "leaked_unverified_total": leaked_total,
            "threshold": THRESHOLD,
        },
        threshold_met=(pass_rate >= THRESHOLD and leaked_total == 0),
    )
    return result
