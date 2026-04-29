"""Offline corpus builder.

Run once locally (or in CI) when seed data changes:

    cd backend
    OPENAI_API_KEY=sk-... python -m scripts.build_corpus

Reads `app.ingest.legal_seed.SEED_DOCS` + `legal_seed_extra.EXTRA_SEED_DOCS`
+ `legal_seed_tier1.TIER1_SEED_DOCS`, calls OpenAI embeddings in batches,
writes `backend/data/corpus.jsonl`. The deployed app loads that file at boot
without any LLM calls.

Output schema (one JSON object per line):
    {"kind": "doc",     "data": {...legal_documents columns + _local_id}}
    {"kind": "chunk",   "data": {...legal_chunks columns + _doc_local_id + embedding}}
    {"kind": "mapping", "data": {old_act, old_section, new_act, new_section, notes}}

Re-running is idempotent (overwrites the file).
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.ingest.embedded_corpus import corpus_file_path
from app.llm.openai_client import embed


def _local_id(doc: dict) -> str:
    """Stable per-doc id derived from short_citation + title."""
    seed = (doc.get("short_citation") or "") + "|" + doc.get("title", "")
    return hashlib.sha1(seed.encode()).hexdigest()[:12]


async def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY required.", file=sys.stderr)
        return 2

    # Lazily import seed modules so import-time errors are visible.
    from app.ingest.legal_seed import SEED_DOCS, SEED_MAPPINGS
    from app.ingest.legal_seed_extra import EXTRA_SEED_DOCS
    try:
        from app.ingest.legal_seed_tier1 import TIER1_SEED_DOCS
    except Exception:
        TIER1_SEED_DOCS = []
    try:
        from app.ingest.legal_seed_phase1 import PHASE1_SEED_DOCS
    except Exception:
        PHASE1_SEED_DOCS = []
    try:
        from app.ingest.legal_seed_constitution import CONSTITUTION_SEED
        CONSTITUTION_DOCS = [CONSTITUTION_SEED]
    except Exception:
        CONSTITUTION_DOCS = []

    all_doc_entries = (
        SEED_DOCS + EXTRA_SEED_DOCS + TIER1_SEED_DOCS
        + PHASE1_SEED_DOCS + CONSTITUTION_DOCS
    )

    out_path = corpus_file_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Dedupe by (short_citation + title); merge their chunks.
    deduped: dict[str, dict] = {}
    for entry in all_doc_entries:
        key = _local_id(entry["doc"])
        if key in deduped:
            deduped[key]["chunks"].extend(entry["chunks"])
        else:
            deduped[key] = {"doc": dict(entry["doc"]), "chunks": list(entry["chunks"])}

    print(f"Building corpus: {len(deduped)} unique docs, "
            f"{sum(len(v['chunks']) for v in deduped.values())} chunks")

    # Collect every chunk text + assign stable refs.
    chunk_records: list[tuple[str, str, dict]] = []
    for local_id, entry in deduped.items():
        for c in entry["chunks"]:
            chunk_records.append((local_id, c["text"], c))

    # Batch-embed (max 96 texts per call to keep payload small).
    BATCH = 64
    embeddings: list[list[float]] = []
    texts = [t for _, t, _ in chunk_records]
    for i in range(0, len(texts), BATCH):
        batch = texts[i:i + BATCH]
        print(f"  embed {i+1}..{i+len(batch)}/{len(texts)}")
        vecs = await embed(batch)
        embeddings.extend(vecs)

    # Write JSONL.
    written = {"docs": 0, "chunks": 0, "mappings": 0}
    with out_path.open("w") as f:
        for local_id, entry in deduped.items():
            doc = dict(entry["doc"])
            doc["_local_id"] = local_id
            f.write(json.dumps({"kind": "doc", "data": doc}, ensure_ascii=False) + "\n")
            written["docs"] += 1

        for (local_id, _, c), vec in zip(chunk_records, embeddings):
            row = {
                "_doc_local_id": local_id,
                "hierarchy_path": c["hierarchy_path"],
                "chunk_type": c["chunk_type"],
                "section_number": c.get("section_number"),
                "text": c["text"],
                "embedding": [round(x, 6) for x in vec],
                "metadata": c.get("metadata", {}),
            }
            f.write(json.dumps({"kind": "chunk", "data": row}, ensure_ascii=False) + "\n")
            written["chunks"] += 1

        for old_act, old_sec, new_act, new_sec, notes in SEED_MAPPINGS:
            f.write(json.dumps({
                "kind": "mapping",
                "data": {"old_act": old_act, "old_section": old_sec,
                          "new_act": new_act, "new_section": new_sec,
                          "notes": notes},
            }) + "\n")
            written["mappings"] += 1

    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"Wrote {out_path} ({size_mb:.2f} MB)")
    print(f"  {written}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
