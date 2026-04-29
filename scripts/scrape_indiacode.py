"""Scrape bare acts from indiacode.nic.in.

We work off the *handle* URL pattern, e.g.
    https://indiacode.nic.in/handle/123456789/2263

Each entry has metadata + downloadable PDF. We pull the PDF, extract text,
chunk by Section using `app.rag.chunker.chunk_statute`, embed, and insert.

Usage:
    python -m scripts.scrape_indiacode --acts BNS,IPC,NI_Act
"""
from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Any

# Catalogue of the highest-value acts. Add more as needed.
# (act_short, india_code_handle_id, title, status_metadata)
ACTS: dict[str, dict[str, Any]] = {
    "BNS":   {"handle": "20062023", "title": "Bharatiya Nyaya Sanhita, 2023",
                "effective_from": "2024-07-01", "status": "in_force"},
    "BNSS":  {"handle": "20063023", "title": "Bharatiya Nagarik Suraksha Sanhita, 2023",
                "effective_from": "2024-07-01", "status": "in_force"},
    "BSA":   {"handle": "20064023", "title": "Bharatiya Sakshya Adhiniyam, 2023",
                "effective_from": "2024-07-01", "status": "in_force"},
    "IPC":   {"handle": "1860-45",   "title": "Indian Penal Code, 1860",
                "effective_to": "2024-06-30", "status": "repealed"},
    "CrPC":  {"handle": "1973-2",    "title": "Code of Criminal Procedure, 1973",
                "effective_to": "2024-06-30", "status": "repealed"},
    "NI_Act":{"handle": "1881-26",   "title": "Negotiable Instruments Act, 1881",
                "status": "in_force"},
    "ContractAct": {"handle": "1872-9", "title": "Indian Contract Act, 1872",
                "status": "in_force"},
    "TPAct": {"handle": "1882-4", "title": "Transfer of Property Act, 1882",
                "status": "in_force"},
    "CPA":   {"handle": "2019-35", "title": "Consumer Protection Act, 2019",
                "status": "in_force"},
    "Companies": {"handle": "2013-18", "title": "Companies Act, 2013",
                "status": "in_force"},
    "DPDP":  {"handle": "2023-22", "title": "Digital Personal Data Protection Act, 2023",
                "status": "in_force"},
    "POSH":  {"handle": "2013-14", "title": "Prevention of Sexual Harassment Act, 2013",
                "status": "in_force"},
    "Arbitration": {"handle": "1996-26", "title": "Arbitration and Conciliation Act, 1996",
                "status": "in_force"},
}


def _index_url(handle: str) -> str:
    # India Code uses opaque handle IDs. The actual landing pattern varies; we
    # build a search URL the scraper resolves to a PDF.
    return f"https://www.indiacode.nic.in/handle/123456789/{handle}"


async def fetch_and_index(act_key: str) -> int:
    from app.db import store
    from app.ingest.text_extract import extract_text
    from app.llm.openai_client import embed
    from app.rag.chunker import chunk_statute
    from scripts._common import fetch

    spec = ACTS.get(act_key)
    if not spec:
        raise SystemExit(f"unknown act key: {act_key}")

    # Try to fetch the landing page; the scraper here is intentionally light —
    # it locates the first PDF link and pulls it. Real-world: extend with the
    # India Code search/listing API.
    url = _index_url(spec["handle"])
    try:
        html = (await fetch(url, ext="html")).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[indiacode] could not fetch {url}: {e}", file=sys.stderr)
        return 0

    pdf_match = re.search(r'href="([^"]+\.pdf)"', html, re.I)
    if not pdf_match:
        print(f"[indiacode] no PDF found at {url}", file=sys.stderr)
        return 0
    pdf_url = pdf_match.group(1)
    if pdf_url.startswith("/"):
        pdf_url = f"https://www.indiacode.nic.in{pdf_url}"

    pdf_bytes = await fetch(pdf_url, ext="pdf")
    text = extract_text(pdf_bytes, "application/pdf")
    chunks = chunk_statute(text, act_short=act_key, act_title=spec["title"], max_tokens=1000)
    if not chunks:
        return 0

    doc = await store.insert_legal_document(
        source_type="central_statute",
        title=spec["title"],
        short_citation=act_key,
        long_citation=spec["title"],
        effective_from=spec.get("effective_from"),
        effective_to=spec.get("effective_to"),
        status=spec.get("status", "in_force"),
        source_url=pdf_url,
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
            metadata={"act_short": act_key, **(chunk.metadata or {})},
        )
    return len(chunks)


async def _main(act_keys: list[str]) -> None:
    total = 0
    for k in act_keys:
        n = await fetch_and_index(k)
        print(f"[indiacode] {k}: {n} chunks")
        total += n
    print(f"[indiacode] done. {total} chunks total.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--acts", default="BNS,NI_Act,ContractAct,TPAct,CPA",
                          help="comma-separated act keys (see ACTS)")
    args = parser.parse_args()
    asyncio.run(_main([k.strip() for k in args.acts.split(",") if k.strip()]))
