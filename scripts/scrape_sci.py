"""Scrape Supreme Court of India judgments.

Strategy: pull the public judgment-search results page for a date range or
docket pattern, follow each judgment URL, extract text, chunk by case anchors,
embed, index.

Usage:
    python -m scripts.scrape_sci --year 2024 --max 100
"""
from __future__ import annotations

import argparse
import asyncio
import re
import sys

SEARCH_URL = "https://judgments.ecourts.gov.in/cnrjudgments/?p={page}&year={year}"


async def crawl_year(year: int, max_judgments: int) -> int:
    from bs4 import BeautifulSoup

    from app.db import store
    from app.llm.openai_client import embed
    from app.rag.chunker import chunk_case
    from scripts._common import fetch

    pulled = 0
    page = 1
    while pulled < max_judgments:
        idx_html = (await fetch(SEARCH_URL.format(page=page, year=year), ext="html"))\
            .decode("utf-8", errors="replace")
        soup = BeautifulSoup(idx_html, "lxml")
        links = [a.get("href") for a in soup.find_all("a", href=True)
                  if a.get("href") and "/judgment/" in a.get("href")]
        if not links:
            break
        for link in links:
            if pulled >= max_judgments:
                break
            url = link if link.startswith("http") else f"https://judgments.ecourts.gov.in{link}"
            try:
                page_html = (await fetch(url, ext="html")).decode("utf-8", errors="replace")
            except Exception as e:
                print(f"[sci] {url} failed: {e}", file=sys.stderr)
                continue
            psoup = BeautifulSoup(page_html, "lxml")
            for tag in psoup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = psoup.get_text("\n", strip=True)
            title = (psoup.title.string if psoup.title else "Supreme Court Judgment").strip()
            citation = _extract_citation(text) or title
            chunks = chunk_case(text, citation=citation, case_name=title, max_tokens=1200)
            if not chunks:
                continue
            doc = await store.insert_legal_document(
                source_type="case",
                title=title[:200],
                short_citation=citation[:100] if citation else None,
                long_citation=citation,
                source_url=url,
                status="in_force",
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
                    metadata=chunk.metadata or {},
                )
            pulled += 1
            if pulled % 10 == 0:
                print(f"[sci] {pulled}/{max_judgments}")
        page += 1
    return pulled


def _extract_citation(text: str) -> str | None:
    m = re.search(r"\bAIR\s+\d{4}\s+SC\s+\d+", text)
    if m:
        return m.group(0)
    m = re.search(r"\(\d{4}\)\s+\d+\s+SCC\s+\d+", text)
    if m:
        return m.group(0)
    return None


async def _main(year: int, max_j: int) -> None:
    n = await crawl_year(year, max_j)
    print(f"[sci] year={year} ingested {n} judgments")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, default=2024)
    p.add_argument("--max", type=int, default=50)
    args = p.parse_args()
    asyncio.run(_main(args.year, args.max))
