"""Shared eval primitives."""
from __future__ import annotations

import asyncio
import dataclasses
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

GOLD_DIR = Path(__file__).parent / "gold"
RESULTS_DIR = Path(__file__).parent / "results"


@dataclass
class EvalResult:
    suite: str
    items: list[dict[str, Any]] = field(default_factory=list)
    aggregate: dict[str, Any] = field(default_factory=dict)
    threshold_met: bool = False
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None

    def add(self, *, id: str, passed: bool, **info: Any) -> None:
        self.items.append({"id": id, "passed": passed, **info})

    def finalize(self, *, aggregate: dict[str, Any], threshold_met: bool) -> None:
        self.aggregate = aggregate
        self.threshold_met = threshold_met
        self.finished_at = time.time()

    def write(self, run_dir: Path) -> Path:
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / f"{self.suite}.json"
        path.write_text(json.dumps({
            "suite": self.suite,
            "aggregate": self.aggregate,
            "threshold_met": self.threshold_met,
            "duration_s": (self.finished_at or time.time()) - self.started_at,
            "n_items": len(self.items),
            "items": self.items,
        }, indent=2, default=str))
        return path

    def print_scorecard(self) -> None:
        passed = sum(1 for i in self.items if i["passed"])
        total = len(self.items)
        status = "PASS" if self.threshold_met else "FAIL"
        print(f"\n[{status}] {self.suite}: {passed}/{total} items passed")
        for k, v in self.aggregate.items():
            print(f"   {k}: {v}")
        if not self.threshold_met:
            failed = [i for i in self.items if not i["passed"]]
            for i in failed[:5]:
                print(f"   FAIL  {i['id']}: {i.get('reason', '')[:120]}")


def load_gold(name: str) -> Iterator[dict[str, Any]]:
    path = GOLD_DIR / f"{name}.jsonl"
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                yield json.loads(line)


async def boot_corpus() -> None:
    """Each suite gets a fresh in-memory corpus seeded with the canonical set."""
    from app.db import store
    from app.ingest.legal_seed import seed_legal_corpus
    store.reset_for_tests()
    await seed_legal_corpus()


def now_run_dir() -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    return RESULTS_DIR / ts


async def gather_bounded(tasks, *, concurrency: int = 4):
    """Run async tasks with bounded concurrency to avoid OpenAI rate limits."""
    sem = asyncio.Semaphore(concurrency)

    async def _run(coro):
        async with sem:
            return await coro

    return await asyncio.gather(*(_run(t) for t in tasks))
