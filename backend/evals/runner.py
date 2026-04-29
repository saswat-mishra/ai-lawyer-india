"""Eval runner CLI.

Usage:
    PYTHONPATH=. python -m evals.runner --suite all
    PYTHONPATH=. python -m evals.runner --suite citation_faithfulness adversarial
"""
from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import os
import sys
import time
from pathlib import Path

from evals._common import RESULTS_DIR, now_run_dir


SUITE_NAMES = [
    "retrieval_recall",
    "citation_faithfulness",
    "refusal",
    "bns_currency",
    "persona",
    "adversarial",
]


async def _run_suite(name: str):
    mod = importlib.import_module(f"evals.suites.{name}")
    return await mod.run()


async def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--suite", nargs="+", default=["all"],
                    help="Suite name(s) or 'all'")
    args = p.parse_args(argv)

    if args.suite == ["all"]:
        suites = SUITE_NAMES
    else:
        suites = []
        for s in args.suite:
            if s == "all":
                suites = SUITE_NAMES
                break
            if s not in SUITE_NAMES:
                print(f"unknown suite: {s} (choose from {SUITE_NAMES})", file=sys.stderr)
                return 2
            suites.append(s)

    if not os.environ.get("OPENAI_API_KEY", "").strip():
        print("OPENAI_API_KEY not set — evals require real OpenAI calls.", file=sys.stderr)
        return 2

    run_dir = now_run_dir()
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"writing results to {run_dir}")

    summary = {"results": [], "started_at": time.time()}
    overall_pass = True
    for s in suites:
        print(f"\n>>> running {s}")
        try:
            res = await _run_suite(s)
        except Exception as e:
            print(f"   ERROR running {s}: {e}")
            overall_pass = False
            continue
        path = res.write(run_dir)
        res.print_scorecard()
        summary["results"].append({
            "suite": s, "threshold_met": res.threshold_met,
            "aggregate": res.aggregate, "path": str(path),
        })
        if not res.threshold_met:
            overall_pass = False

    summary["overall_pass"] = overall_pass
    summary["finished_at"] = time.time()
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(f"\n{'=' * 60}\noverall: {'PASS' if overall_pass else 'FAIL'}\n{'=' * 60}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
