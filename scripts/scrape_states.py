"""State-statute scraper.

Maharashtra, Delhi, Karnataka first; remainder by population (UP, MP, TN, WB,
Bihar, Rajasthan, ...).

Each state has a different listing convention; this script reads a YAML manifest
keyed by state code, resolves each entry to a downloadable PDF, and ingests.

Usage:
    python -m scripts.scrape_states --states MH,DL,KA
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Inline manifest. Add entries as we identify authoritative URLs per state.
# (state_code, [(act_short, title, url, status)])
STATE_MANIFEST: dict[str, list[dict]] = {
    "MH": [
        {"short": "MRCA-1999", "title": "Maharashtra Rent Control Act, 1999",
          "url": "https://lj.maharashtra.gov.in/Site/Upload/Acts/MRCA1999.pdf",
          "status": "in_force"},
        {"short": "MaharashtraStamp", "title": "Maharashtra Stamp Act",
          "url": "https://igrmaharashtra.gov.in/SB_LATESTAMENDMENTS/MAH_STAMP_ACT.pdf",
          "status": "in_force"},
    ],
    "DL": [
        {"short": "DRCA-1958", "title": "Delhi Rent Control Act, 1958",
          "url": "https://www.indiacode.nic.in/bitstream/123456789/4925/1/A1958-59.pdf",
          "status": "in_force"},
    ],
    "KA": [
        {"short": "KRA-1999", "title": "Karnataka Rent Act, 1999",
          "url": "https://dpal.karnataka.gov.in/storage/pdf-files/KarnatakaRentAct1999.pdf",
          "status": "in_force"},
    ],
    # Phase 2 — populate from indiacode.nic.in/state-acts.
    "UP": [], "TN": [], "WB": [], "MP": [], "RJ": [], "BR": [], "GJ": [],
    "TS": [], "AP": [], "PB": [], "HR": [], "OR": [], "KL": [], "AS": [],
    "JH": [], "CG": [], "UK": [], "HP": [], "GA": [], "TR": [], "MN": [],
    "ML": [], "NL": [], "AR": [], "MZ": [], "SK": [],
}


async def ingest_state(state_code: str) -> int:
    from app.db import store
    from app.ingest.text_extract import extract_text
    from app.llm.openai_client import embed
    from app.rag.chunker import chunk_statute
    from scripts._common import fetch

    entries = STATE_MANIFEST.get(state_code, [])
    if not entries:
        print(f"[states] {state_code} has no manifest entries yet", file=sys.stderr)
        return 0
    total = 0
    for entry in entries:
        try:
            pdf = await fetch(entry["url"], ext="pdf")
        except Exception as e:
            print(f"[states] {entry['short']} fetch failed: {e}", file=sys.stderr)
            continue
        text = extract_text(pdf, "application/pdf")
        chunks = chunk_statute(text, act_short=entry["short"], act_title=entry["title"])
        if not chunks:
            continue
        doc = await store.insert_legal_document(
            source_type="state_statute",
            jurisdiction=state_code,
            title=entry["title"],
            short_citation=entry["short"],
            long_citation=entry["title"],
            status=entry.get("status", "in_force"),
            source_url=entry["url"],
        )
        embeddings = await embed([c.text for c in chunks])
        for chunk, vec in zip(chunks, embeddings):
            await store.insert_legal_chunk(
                document_id=doc["id"],
                hierarchy_path=chunk.hierarchy_path,
                chunk_type=chunk.chunk_type,
                section_number=chunk.section_number,
                text=chunk.text,
                embedding=vec,
                metadata={"state": state_code, "act_short": entry["short"]},
            )
        total += len(chunks)
        print(f"[states] {state_code}/{entry['short']}: {len(chunks)} chunks")
    return total


async def _main(states: list[str]) -> None:
    grand = 0
    for s in states:
        grand += await ingest_state(s.upper())
    print(f"[states] total chunks: {grand}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--states", default="MH,DL,KA", help="comma-separated state codes")
    args = p.parse_args()
    asyncio.run(_main([s.strip() for s in args.states.split(",") if s.strip()]))
