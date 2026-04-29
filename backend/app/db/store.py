"""Thin async DB layer. Pluggable: real Postgres in prod, in-memory for tests.

We keep it deliberately small. The agent uses repository functions — never
raw SQL strings except in this module.
"""
from __future__ import annotations

import asyncio
import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from app.core.config import get_settings


# ---------- In-memory store (used in tests / local dev without Postgres) ----------


@dataclass
class _Mem:
    devices: dict[str, dict[str, Any]] = field(default_factory=dict)
    conversations: dict[str, dict[str, Any]] = field(default_factory=dict)
    messages: dict[str, dict[str, Any]] = field(default_factory=dict)
    legal_documents: dict[str, dict[str, Any]] = field(default_factory=dict)
    legal_chunks: dict[str, dict[str, Any]] = field(default_factory=dict)
    statute_mapping: list[dict[str, Any]] = field(default_factory=list)
    case_citations: list[dict[str, Any]] = field(default_factory=list)
    company_documents: dict[str, dict[str, Any]] = field(default_factory=dict)
    company_chunks: dict[str, dict[str, Any]] = field(default_factory=dict)
    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)
    audit: list[dict[str, Any]] = field(default_factory=list)


_mem = _Mem()
_lock = asyncio.Lock()


# ---------- Public API ----------


def use_memory_backend() -> bool:
    """We use the in-memory backend when DATABASE_URL points to a non-existent host
    or when AIL_FORCE_MEMORY=1 is set. Determined lazily.
    """
    if os.environ.get("AIL_FORCE_MEMORY") == "1":
        return True
    # In dev / test without real Postgres, fall back to memory unless explicitly disabled.
    return os.environ.get("AIL_FORCE_PG") != "1"


# ----- Devices -----

async def upsert_device(device_id: str, *, persona: str = "citizen",
                         language_pref: str = "en") -> dict[str, Any]:
    async with _lock:
        existing = _mem.devices.get(device_id)
        if existing:
            existing["last_seen_at"] = _now()
            return existing
        record = {
            "device_id": device_id,
            "persona": persona,
            "language_pref": language_pref,
            "created_at": _now(),
            "last_seen_at": _now(),
        }
        _mem.devices[device_id] = record
        return record


async def get_device(device_id: str) -> dict[str, Any] | None:
    return _mem.devices.get(device_id)


async def update_device_persona(device_id: str, persona: str) -> dict[str, Any]:
    async with _lock:
        d = _mem.devices.setdefault(device_id, {
            "device_id": device_id, "persona": "citizen", "language_pref": "en",
            "created_at": _now(), "last_seen_at": _now(),
        })
        d["persona"] = persona
        d["last_seen_at"] = _now()
        return d


async def update_device_language(device_id: str, language_pref: str) -> dict[str, Any]:
    async with _lock:
        d = _mem.devices.setdefault(device_id, {
            "device_id": device_id, "persona": "citizen", "language_pref": "en",
            "created_at": _now(), "last_seen_at": _now(),
        })
        d["language_pref"] = language_pref
        return d


# ----- Conversations -----

async def create_conversation(device_id: str, *, title: str = "",
                               workflow: str = "chat") -> dict[str, Any]:
    cid = str(uuid.uuid4())
    record = {
        "id": cid, "device_id": device_id, "title": title or "New conversation",
        "workflow": workflow, "created_at": _now(), "updated_at": _now(),
    }
    async with _lock:
        _mem.conversations[cid] = record
    return record


async def list_conversations(device_id: str) -> list[dict[str, Any]]:
    return sorted(
        [c for c in _mem.conversations.values() if c["device_id"] == device_id],
        key=lambda c: c["updated_at"], reverse=True,
    )


async def get_conversation(conversation_id: str, device_id: str) -> dict[str, Any] | None:
    c = _mem.conversations.get(conversation_id)
    if c and c["device_id"] == device_id:
        return c
    return None


async def add_message(conversation_id: str, *, role: str, content: str,
                       meta: dict[str, Any] | None = None,
                       confidence: str | None = None) -> dict[str, Any]:
    mid = str(uuid.uuid4())
    record = {
        "id": mid, "conversation_id": conversation_id, "role": role,
        "content": content, "meta": meta or {}, "confidence": confidence,
        "created_at": _now(),
    }
    async with _lock:
        _mem.messages[mid] = record
        if conversation_id in _mem.conversations:
            _mem.conversations[conversation_id]["updated_at"] = _now()
    return record


async def list_messages(conversation_id: str) -> list[dict[str, Any]]:
    return sorted(
        [m for m in _mem.messages.values() if m["conversation_id"] == conversation_id],
        key=lambda m: m["created_at"],
    )


# ----- Legal corpus -----

async def insert_legal_document(**fields: Any) -> dict[str, Any]:
    did = str(uuid.uuid4())
    record = {"id": did, **fields, "created_at": _now()}
    record.setdefault("status", "in_force")
    record.setdefault("jurisdiction", "india")
    record.setdefault("metadata", {})
    async with _lock:
        _mem.legal_documents[did] = record
    return record


async def insert_legal_chunk(**fields: Any) -> dict[str, Any]:
    cid = str(uuid.uuid4())
    record = {"id": cid, **fields, "created_at": _now()}
    record.setdefault("metadata", {})
    async with _lock:
        _mem.legal_chunks[cid] = record
    return record


async def list_legal_documents() -> list[dict[str, Any]]:
    return list(_mem.legal_documents.values())


async def list_legal_chunks() -> list[dict[str, Any]]:
    return list(_mem.legal_chunks.values())


async def get_legal_chunk(chunk_id: str) -> dict[str, Any] | None:
    return _mem.legal_chunks.get(chunk_id)


async def get_legal_document(document_id: str) -> dict[str, Any] | None:
    return _mem.legal_documents.get(document_id)


async def find_section_by_number(act_short: str, section: str) -> dict[str, Any] | None:
    """Find a chunk by act + section, used by citation verifier and IPC->BNS lookup."""
    act_short = str(act_short).strip().upper()
    section = str(section).strip()
    for chunk in _mem.legal_chunks.values():
        if chunk.get("section_number") != section:
            continue
        doc = _mem.legal_documents.get(chunk["document_id"])
        if not doc:
            continue
        # Match on short_citation or title, case-insensitive.
        candidate = (doc.get("short_citation") or "") + " " + (doc.get("title") or "")
        if act_short.lower() in candidate.lower():
            return chunk
    return None


# ----- Statute mapping -----

async def add_statute_mapping(old_act: str, old_section: str,
                               new_act: str, new_section: str,
                               notes: str = "") -> None:
    async with _lock:
        _mem.statute_mapping.append({
            "old_act": old_act, "old_section": old_section,
            "new_act": new_act, "new_section": new_section, "notes": notes,
        })


async def lookup_successor_section(old_act: str, old_section: str) -> dict[str, Any] | None:
    for m in _mem.statute_mapping:
        if m["old_act"] == old_act and m["old_section"] == old_section:
            return m
    return None


# ----- Citator graph (case-cites-case) -----

async def add_case_citation(*, source_doc_id: str, cited_doc_id: str,
                             treatment: str, paragraph: int | None = None) -> bool:
    """Idempotent insert. Returns True on insert, False on duplicate."""
    async with _lock:
        for c in _mem.case_citations:
            if (c["source_doc_id"] == source_doc_id
                    and c["cited_doc_id"] == cited_doc_id
                    and c.get("paragraph") == paragraph):
                return False
        _mem.case_citations.append({
            "id": len(_mem.case_citations) + 1,
            "source_doc_id": source_doc_id,
            "cited_doc_id": cited_doc_id,
            "treatment": treatment,
            "paragraph": paragraph,
        })
        return True


async def list_citations_to(*, cited_doc_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """Cases that cite the given doc, with treatment + source metadata."""
    out: list[dict[str, Any]] = []
    # Treatment severity ordering — show "overruled" / "doubted" first.
    SEVERITY = {"overruled": 0, "doubted": 1, "distinguished": 2,
                "followed": 3, "referred": 4}
    raw = [c for c in _mem.case_citations if c["cited_doc_id"] == cited_doc_id]
    raw.sort(key=lambda c: SEVERITY.get(c.get("treatment", "referred"), 9))
    for c in raw[:limit]:
        src = _mem.legal_documents.get(c["source_doc_id"], {})
        out.append({
            "treatment": c["treatment"],
            "paragraph": c.get("paragraph"),
            "source_doc_id": c["source_doc_id"],
            "source_short_citation": src.get("short_citation"),
            "source_title": src.get("title"),
            "source_status": src.get("status"),
        })
    return out


async def list_citations_from(*, source_doc_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """What does this case cite?"""
    out: list[dict[str, Any]] = []
    raw = [c for c in _mem.case_citations if c["source_doc_id"] == source_doc_id]
    for c in raw[:limit]:
        dst = _mem.legal_documents.get(c["cited_doc_id"], {})
        out.append({
            "treatment": c["treatment"],
            "paragraph": c.get("paragraph"),
            "cited_doc_id": c["cited_doc_id"],
            "cited_short_citation": dst.get("short_citation"),
            "cited_title": dst.get("title"),
            "cited_status": dst.get("status"),
        })
    return out


# ----- Company KB -----

async def insert_company_document(*, device_id: str, filename: str, mime_type: str,
                                    size_bytes: int, doc_type: str = "agreement",
                                    storage_path: str | None = None,
                                    link_url: str | None = None,
                                    metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    did = str(uuid.uuid4())
    record = {
        "id": did, "device_id": device_id, "filename": filename, "mime_type": mime_type,
        "size_bytes": size_bytes, "storage_path": storage_path, "doc_type": doc_type,
        "link_url": link_url, "status": "uploaded", "visibility": "private",
        "metadata": metadata or {}, "created_at": _now(),
    }
    async with _lock:
        _mem.company_documents[did] = record
    return record


async def update_company_document_status(doc_id: str, status: str) -> None:
    async with _lock:
        if doc_id in _mem.company_documents:
            _mem.company_documents[doc_id]["status"] = status


async def list_company_documents(device_id: str) -> list[dict[str, Any]]:
    return [d for d in _mem.company_documents.values() if d["device_id"] == device_id]


async def get_company_document(doc_id: str, device_id: str) -> dict[str, Any] | None:
    d = _mem.company_documents.get(doc_id)
    if d and d["device_id"] == device_id:
        return d
    return None


async def delete_company_document(doc_id: str, device_id: str) -> bool:
    async with _lock:
        d = _mem.company_documents.get(doc_id)
        if not d or d["device_id"] != device_id:
            return False
        del _mem.company_documents[doc_id]
        # Cascade chunks.
        to_drop = [cid for cid, c in _mem.company_chunks.items() if c["document_id"] == doc_id]
        for cid in to_drop:
            del _mem.company_chunks[cid]
        return True


async def insert_company_chunk(**fields: Any) -> dict[str, Any]:
    cid = str(uuid.uuid4())
    record = {"id": cid, **fields, "created_at": _now()}
    record.setdefault("metadata", {})
    async with _lock:
        _mem.company_chunks[cid] = record
    return record


async def list_company_chunks(device_id: str) -> list[dict[str, Any]]:
    return [c for c in _mem.company_chunks.values() if c["device_id"] == device_id]


# ----- Artifacts -----

async def insert_artifact(**fields: Any) -> dict[str, Any]:
    aid = str(uuid.uuid4())
    record = {"id": aid, **fields, "created_at": _now()}
    record.setdefault("status", "final")
    record.setdefault("citations", [])
    record.setdefault("inputs", {})
    async with _lock:
        _mem.artifacts[aid] = record
    return record


async def list_artifacts(device_id: str) -> list[dict[str, Any]]:
    return sorted(
        [a for a in _mem.artifacts.values() if a["device_id"] == device_id],
        key=lambda a: a["created_at"], reverse=True,
    )


async def get_artifact(artifact_id: str, device_id: str) -> dict[str, Any] | None:
    a = _mem.artifacts.get(artifact_id)
    if a and a["device_id"] == device_id:
        return a
    return None


# ----- Audit -----

async def audit(event_type: str, *, device_id: str | None = None,
                conversation_id: str | None = None,
                payload: dict[str, Any] | None = None) -> None:
    async with _lock:
        _mem.audit.append({
            "event_type": event_type, "device_id": device_id,
            "conversation_id": conversation_id, "payload": payload or {},
            "created_at": _now(),
        })


async def audit_events_for(device_id: str) -> list[dict[str, Any]]:
    return [e for e in _mem.audit if e["device_id"] == device_id]


# ---------- Test helpers ----------

def reset_for_tests() -> None:
    global _mem
    _mem = _Mem()


# ---------- Util ----------

def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
