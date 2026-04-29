"""Pre-embedded corpus loader.

Vercel serverless cold-start budget is tight. Embedding hundreds of chunks
synchronously at boot would (a) blow the function timeout and (b) cost real
money. Instead we ship a `data/corpus.jsonl` file containing every chunk's
text + pre-computed embedding. At boot we just load the JSONL into the
in-memory store — no API calls, no latency.

The pipeline:
1. `scripts/build_corpus.py` (offline, run by maintainer) reads the seed dicts
   in `legal_seed*.py`, calls OpenAI embeddings once, writes
   `backend/data/corpus.jsonl`.
2. This module reads that file at app startup. If the file is missing, it
   falls back to the live-embedding path (`legal_seed.seed_legal_corpus`).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.db import store


_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_CORPUS_FILE = _DATA_DIR / "corpus.jsonl"


def corpus_file_path() -> Path:
    return _CORPUS_FILE


async def load_pre_embedded_corpus() -> dict[str, int]:
    """Load every chunk + embedding from the JSONL bundle.

    Returns counts for visibility. Returns {"loaded": False} when the file
    is absent so the caller can fall back to live embedding.
    """
    if not _CORPUS_FILE.exists():
        return {"loaded": False}

    docs_seen: dict[str, str] = {}
    n_chunks = 0
    n_mappings = 0
    with _CORPUS_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            kind = row.get("kind")
            if kind == "doc":
                d = row["data"]
                doc = await store.insert_legal_document(**d)
                docs_seen[d.get("_local_id", d["title"])] = doc["id"]
            elif kind == "chunk":
                c = row["data"]
                local_doc_id = c.pop("_doc_local_id", None)
                doc_id = docs_seen.get(local_doc_id) if local_doc_id else None
                if not doc_id:
                    # Fallback: match by short_citation if present in metadata.
                    continue
                await store.insert_legal_chunk(
                    document_id=doc_id,
                    hierarchy_path=c["hierarchy_path"],
                    chunk_type=c["chunk_type"],
                    section_number=c.get("section_number"),
                    text=c["text"],
                    embedding=c["embedding"],
                    metadata=c.get("metadata", {}),
                )
                n_chunks += 1
            elif kind == "mapping":
                m = row["data"]
                await store.add_statute_mapping(
                    m["old_act"], m["old_section"],
                    m["new_act"], m["new_section"],
                    m.get("notes", ""),
                )
                n_mappings += 1
    return {"loaded": True, "docs": len(docs_seen), "chunks": n_chunks,
              "mappings": n_mappings}
