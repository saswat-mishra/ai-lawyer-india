"""Retrieval recall using REAL embeddings.

For each gold query, embed via OpenAI, run hybrid retrieval, check whether
the expected (act, section) chunk lands in top-1, top-3, top-5.
"""
from __future__ import annotations

from app.core.config import Persona
from app.rag.retriever import retrieve_legal
from evals._common import EvalResult, boot_corpus, load_gold


THRESHOLD_R5 = 0.85


async def run() -> EvalResult:
    await boot_corpus()
    result = EvalResult(suite="retrieval_recall")

    hits = {1: 0, 3: 0, 5: 0}
    n = 0
    for entry in load_gold("retrieval_recall"):
        n += 1
        out = await retrieve_legal(entry["query"], persona=Persona.PRACTITIONER)
        section_hits = []
        for k in (1, 3, 5):
            top_k = out[:k]
            ok = False
            if "expect_section" in entry:
                ok = any(c.section_number == entry["expect_section"]
                            and (entry.get("expect_act", "").lower()
                                  in " ".join(c.hierarchy_path).lower())
                            for c in top_k)
            elif "expect_chunk_type" in entry:
                ok = any(c.chunk_type == entry["expect_chunk_type"] for c in top_k)
            if ok:
                hits[k] += 1
                section_hits.append(k)
        passed = 5 in section_hits
        result.add(
            id=entry["id"], passed=passed,
            in_top1=1 in section_hits,
            in_top3=3 in section_hits,
            in_top5=5 in section_hits,
            top1_section=(out[0].section_number if out else None),
            top1_path=(" > ".join(out[0].hierarchy_path) if out else None),
            reason=("ok" if passed else "expected chunk not in top-5"),
        )

    r1 = hits[1] / n if n else 0
    r3 = hits[3] / n if n else 0
    r5 = hits[5] / n if n else 0
    result.finalize(
        aggregate={"n": n, "recall@1": round(r1, 3), "recall@3": round(r3, 3),
                    "recall@5": round(r5, 3), "threshold@5": THRESHOLD_R5},
        threshold_met=(r5 >= THRESHOLD_R5),
    )
    return result
