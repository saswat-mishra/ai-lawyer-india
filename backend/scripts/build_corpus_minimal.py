"""Minimal corpus builder — no pydantic / openai-sdk dependency.

Uses urllib + the OpenAI REST API directly. Designed to run in constrained
sandboxes where we can't pip-install the full project deps. Output schema
matches scripts/build_corpus.py exactly so the deployed app can load it.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
OUT = DATA_DIR / "corpus.jsonl"


def _load(modname: str, path: Path):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _local_id(doc: dict) -> str:
    seed = (doc.get("short_citation") or "") + "|" + doc.get("title", "")
    return hashlib.sha1(seed.encode()).hexdigest()[:12]


def _read_dotenv():
    env_path = ROOT.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def embed_batch(texts: list[str], *, model: str = "text-embedding-3-small") -> list[list[float]]:
    """POST to OpenAI embeddings via urllib — no sdk needed."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    body = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            return [d["embedding"] for d in data["data"]]
        except Exception as e:
            if attempt == 2:
                raise
            print(f"  embed attempt {attempt+1} failed: {e!r}; retrying", file=sys.stderr)
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def main() -> int:
    _read_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY required.", file=sys.stderr)
        return 2

    seed_dir = ROOT / "app" / "ingest"
    # Load the data-only seed modules. legal_seed.py imports app.db.store
    # (pydantic), so we load just SEED_DOCS / SEED_MAPPINGS via AST eval.
    mods = {
        "SEED_DOCS": ("legal_seed.py", True),
        "EXTRA_SEED_DOCS": ("legal_seed_extra.py", False),
        "TIER1_SEED_DOCS": ("legal_seed_tier1.py", False),
        "PHASE1_SEED_DOCS": ("legal_seed_phase1.py", False),
        "CONSTITUTION_SEED": ("legal_seed_constitution.py", False),
        "CASE_SEED_DOCS": ("legal_seed_cases.py", False),
        "PHASE2_SEED_DOCS": ("legal_seed_phase2.py", False),
    }
    SEED_MAPPINGS = []
    all_doc_entries: list[dict] = []
    for var, (fname, has_app_dep) in mods.items():
        path = seed_dir / fname
        if not path.exists():
            continue
        if has_app_dep:
            # Pull SEED_DOCS / SEED_MAPPINGS via a controlled exec without
            # importing app.db.store. We monkeypatch the missing module.
            src = path.read_text()
            # Strip the `from app.db import store` and `from app.llm.openai_client import embed`
            patched = src.replace("from app.db import store", "store = None")
            patched = patched.replace("from app.llm.openai_client import embed", "async def embed(*a, **kw): return []")
            # Remove the seeder coroutine — only need data.
            ns: dict = {}
            try:
                exec(patched, ns, ns)
            except Exception as e:
                print(f"FATAL: cannot load {fname}: {e}", file=sys.stderr)
                return 3
            if "SEED_DOCS" in ns:
                all_doc_entries.extend(ns["SEED_DOCS"])
            if "SEED_MAPPINGS" in ns:
                SEED_MAPPINGS.extend(ns["SEED_MAPPINGS"])
            continue
        m = _load(fname.replace(".py", ""), path)
        val = getattr(m, var, None)
        if val is None:
            continue
        if isinstance(val, list):
            all_doc_entries.extend(val)
        else:
            all_doc_entries.append(val)

    # Dedupe by (short_citation + title); merge their chunks.
    deduped: dict[str, dict] = {}
    for entry in all_doc_entries:
        k = _local_id(entry["doc"])
        if k in deduped:
            deduped[k]["chunks"].extend(entry["chunks"])
        else:
            deduped[k] = {"doc": dict(entry["doc"]), "chunks": list(entry["chunks"])}

    n_docs = len(deduped)
    n_chunks = sum(len(v["chunks"]) for v in deduped.values())
    print(f"Building corpus: {n_docs} unique docs, {n_chunks} chunks")
    print(f"  Mappings: {len(SEED_MAPPINGS)}")

    # Embed in batches.
    chunk_records = []
    for local_id, entry in deduped.items():
        for c in entry["chunks"]:
            chunk_records.append((local_id, c))
    BATCH = 64
    embeddings: list[list[float]] = []
    for i in range(0, len(chunk_records), BATCH):
        batch_texts = [c["text"] for _, c in chunk_records[i:i + BATCH]]
        print(f"  embed {i+1}..{i+len(batch_texts)}/{n_chunks}")
        vecs = embed_batch(batch_texts)
        embeddings.extend(vecs)

    # Write JSONL.
    written = {"docs": 0, "chunks": 0, "mappings": 0}
    with OUT.open("w") as f:
        for local_id, entry in deduped.items():
            doc = dict(entry["doc"])
            doc["_local_id"] = local_id
            f.write(json.dumps({"kind": "doc", "data": doc}, ensure_ascii=False) + "\n")
            written["docs"] += 1
        for (local_id, c), vec in zip(chunk_records, embeddings):
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
                         "new_act": new_act, "new_section": new_sec, "notes": notes},
            }) + "\n")
            written["mappings"] += 1

        # Citator graph — load KNOWN_TREATMENTS and emit as 'citation' rows.
        try:
            cit_mod = _load("citator", ROOT / "app" / "rag" / "citator.py")
            for src_cite, dst_cite, treatment, para in cit_mod.KNOWN_TREATMENTS:
                f.write(json.dumps({
                    "kind": "citation",
                    "data": {
                        "source_citation": src_cite,
                        "cited_citation": dst_cite,
                        "treatment": treatment,
                        "paragraph": para,
                    },
                }) + "\n")
                written["citations"] = written.get("citations", 0) + 1
        except Exception as e:
            print(f"  citator emit failed: {e}", file=sys.stderr)

    size_mb = OUT.stat().st_size / 1024 / 1024
    print(f"Wrote {OUT} ({size_mb:.2f} MB)")
    print(f"  {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
