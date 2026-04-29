"""Postgres-backed implementation of the same async interface as `store.py`.

Selected when DATABASE_URL points at a real Postgres (i.e., not the in-memory
fallback). Used in Vercel serverless where in-memory state would be lost
between invocations.

We keep the surface minimal — only the operations the API actually invokes.
Anything more advanced (citator graph, audit complete export) can be added
incrementally; this is the production critical path.
"""
from __future__ import annotations

import asyncio
import json
import os
import uuid
from typing import Any

try:
    import asyncpg
except ImportError:  # asyncpg is optional in dev / test
    asyncpg = None  # type: ignore[assignment]


_pool: "asyncpg.Pool | None" = None
_pool_lock = asyncio.Lock()


async def _get_pool() -> "asyncpg.Pool":
    global _pool
    if _pool is not None:
        return _pool
    async with _pool_lock:
        if _pool is not None:
            return _pool
        if asyncpg is None:
            raise RuntimeError("asyncpg is not installed but pg_store was selected")
        dsn = os.environ.get("DATABASE_URL")
        if not dsn:
            raise RuntimeError("DATABASE_URL is required for pg_store")
        _pool = await asyncpg.create_pool(dsn, min_size=1, max_size=4,
                                              command_timeout=30,
                                              statement_cache_size=0)
        return _pool


def _vec_literal(vec: list[float]) -> str:
    """pgvector wire format: '[0.1, 0.2, ...]'."""
    return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"


# ---------- Devices ----------

async def upsert_device(device_id: str, *, persona: str = "citizen",
                         language_pref: str = "en") -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into devices(device_id, persona, language_pref)
            values ($1, $2, $3)
            on conflict (device_id) do update set last_seen_at = now()
            returning device_id::text, persona, language_pref,
                      created_at::text, last_seen_at::text;
        """, uuid.UUID(device_id), persona, language_pref)
    return dict(row)


async def get_device(device_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select device_id::text, persona, language_pref,
                   created_at::text, last_seen_at::text
            from devices where device_id = $1
        """, uuid.UUID(device_id))
    return dict(row) if row else None


async def update_device_persona(device_id: str, persona: str) -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into devices(device_id, persona) values ($1, $2)
            on conflict (device_id) do update set persona = excluded.persona,
                                                  last_seen_at = now()
            returning device_id::text, persona, language_pref,
                      created_at::text, last_seen_at::text;
        """, uuid.UUID(device_id), persona)
    return dict(row)


async def update_device_language(device_id: str, language_pref: str) -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into devices(device_id, language_pref) values ($1, $2)
            on conflict (device_id) do update set language_pref = excluded.language_pref,
                                                  last_seen_at = now()
            returning device_id::text, persona, language_pref,
                      created_at::text, last_seen_at::text;
        """, uuid.UUID(device_id), language_pref)
    return dict(row)


# ---------- Conversations ----------

async def create_conversation(device_id: str, *, title: str = "",
                                workflow: str = "chat") -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into conversations(device_id, title, workflow)
            values ($1, $2, $3)
            returning id::text, device_id::text, title, workflow,
                      created_at::text, updated_at::text;
        """, uuid.UUID(device_id), title or "New conversation", workflow)
    return dict(row)


async def list_conversations(device_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, device_id::text, title, workflow,
                   created_at::text, updated_at::text
            from conversations where device_id = $1
            order by updated_at desc
        """, uuid.UUID(device_id))
    return [dict(r) for r in rows]


async def get_conversation(conversation_id: str, device_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select id::text, device_id::text, title, workflow,
                   created_at::text, updated_at::text
            from conversations where id = $1 and device_id = $2
        """, uuid.UUID(conversation_id), uuid.UUID(device_id))
    return dict(row) if row else None


# ---------- Messages ----------

async def add_message(conversation_id: str, *, role: str, content: str,
                       meta: dict[str, Any] | None = None,
                       confidence: str | None = None) -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into messages(conversation_id, role, content, meta, confidence)
            values ($1, $2, $3, $4::jsonb, $5)
            returning id::text, conversation_id::text, role, content,
                      meta, confidence, created_at::text
        """, uuid.UUID(conversation_id), role, content,
             json.dumps(meta or {}), confidence)
    return _row_with_meta(row)


async def list_messages(conversation_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, conversation_id::text, role, content,
                   meta, confidence, created_at::text
            from messages where conversation_id = $1 order by created_at
        """, uuid.UUID(conversation_id))
    return [_row_with_meta(r) for r in rows]


def _row_with_meta(row) -> dict[str, Any]:
    d = dict(row)
    if isinstance(d.get("meta"), str):
        try:
            d["meta"] = json.loads(d["meta"])
        except Exception:
            pass
    return d


# ---------- Legal corpus ----------

async def insert_legal_document(**fields: Any) -> dict[str, Any]:
    pool = await _get_pool()
    fields.setdefault("status", "in_force")
    fields.setdefault("jurisdiction", "india")
    fields.setdefault("metadata", {})
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into legal_documents(source_type, jurisdiction, title,
              short_citation, long_citation, effective_from, effective_to,
              status, source_url, metadata)
            values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb)
            returning id::text, source_type, jurisdiction, title,
                      short_citation, long_citation, status, source_url,
                      metadata, created_at::text
        """, fields["source_type"], fields["jurisdiction"], fields["title"],
             fields.get("short_citation"), fields.get("long_citation"),
             fields.get("effective_from"), fields.get("effective_to"),
             fields["status"], fields.get("source_url"),
             json.dumps(fields["metadata"]))
    return _row_with_meta(row)


async def insert_legal_chunk(**fields: Any) -> dict[str, Any]:
    pool = await _get_pool()
    metadata = fields.get("metadata", {})
    embedding = fields.get("embedding")
    emb_lit = _vec_literal(embedding) if embedding else None
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into legal_chunks(document_id, hierarchy_path, chunk_type,
              section_number, text, token_count, embedding, metadata)
            values ($1, $2, $3, $4, $5, $6, $7::vector, $8::jsonb)
            returning id::text, document_id::text, hierarchy_path, chunk_type,
                      section_number, text, metadata, created_at::text
        """, uuid.UUID(fields["document_id"]),
             fields["hierarchy_path"], fields["chunk_type"],
             fields.get("section_number"), fields["text"],
             fields.get("token_count"), emb_lit, json.dumps(metadata))
    out = _row_with_meta(row)
    out["embedding"] = embedding
    return out


async def list_legal_documents() -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, source_type, jurisdiction, title,
                   short_citation, long_citation, status, source_url,
                   metadata, created_at::text
            from legal_documents
        """)
    return [_row_with_meta(r) for r in rows]


async def list_legal_chunks() -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, document_id::text, hierarchy_path, chunk_type,
                   section_number, text, embedding::text as embedding_text,
                   metadata, created_at::text
            from legal_chunks
        """)
    out = []
    for r in rows:
        d = _row_with_meta(r)
        emb_text = d.pop("embedding_text", None)
        d["embedding"] = _parse_vec(emb_text) if emb_text else None
        out.append(d)
    return out


async def get_legal_chunk(chunk_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select id::text, document_id::text, hierarchy_path, chunk_type,
                   section_number, text, embedding::text as embedding_text,
                   metadata, created_at::text
            from legal_chunks where id = $1
        """, uuid.UUID(chunk_id))
    if not row:
        return None
    d = _row_with_meta(row)
    emb_text = d.pop("embedding_text", None)
    d["embedding"] = _parse_vec(emb_text) if emb_text else None
    return d


async def get_legal_document(document_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select id::text, source_type, jurisdiction, title,
                   short_citation, long_citation, status, source_url,
                   metadata, created_at::text
            from legal_documents where id = $1
        """, uuid.UUID(document_id))
    return _row_with_meta(row) if row else None


async def find_section_by_number(act_short: str, section: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select c.id::text, c.document_id::text, c.hierarchy_path,
                   c.chunk_type, c.section_number, c.text,
                   c.metadata, c.created_at::text
            from legal_chunks c
            join legal_documents d on d.id = c.document_id
            where c.section_number = $1
              and (lower(coalesce(d.short_citation,'')) like '%' || lower($2) || '%'
                   or lower(coalesce(d.title,'')) like '%' || lower($2) || '%')
            limit 1
        """, section, act_short)
    return _row_with_meta(row) if row else None


def _parse_vec(s: str | None) -> list[float] | None:
    if not s:
        return None
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [float(x) for x in s.split(",") if x.strip()]


# ---------- Statute mapping ----------

async def add_statute_mapping(old_act: str, old_section: str,
                                new_act: str, new_section: str,
                                notes: str = "") -> None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        await c.execute("""
            insert into statute_section_mapping(old_act, old_section, new_act, new_section, notes)
            values ($1, $2, $3, $4, $5) on conflict do nothing
        """, old_act, old_section, new_act, new_section, notes)


async def lookup_successor_section(old_act: str, old_section: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select old_act, old_section, new_act, new_section, notes
            from statute_section_mapping
            where old_act = $1 and old_section = $2 limit 1
        """, old_act, old_section)
    return dict(row) if row else None


# ---------- Company KB (per-device namespace) ----------

async def insert_company_document(*, device_id: str, filename: str, mime_type: str,
                                    size_bytes: int, doc_type: str = "agreement",
                                    storage_path: str | None = None,
                                    link_url: str | None = None,
                                    metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into company_documents(device_id, filename, mime_type,
              size_bytes, storage_path, doc_type, link_url, metadata)
            values ($1, $2, $3, $4, $5, $6, $7, $8::jsonb)
            returning id::text, device_id::text, filename, mime_type,
                      size_bytes, storage_path, doc_type, link_url, status,
                      visibility, metadata, created_at::text
        """, uuid.UUID(device_id), filename, mime_type, size_bytes,
             storage_path, doc_type, link_url, json.dumps(metadata or {}))
    return _row_with_meta(row)


async def update_company_document_status(doc_id: str, status: str) -> None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        await c.execute("update company_documents set status = $1 where id = $2",
                          status, uuid.UUID(doc_id))


async def list_company_documents(device_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, device_id::text, filename, mime_type, size_bytes,
                   storage_path, doc_type, link_url, status, visibility,
                   metadata, created_at::text
            from company_documents where device_id = $1
            order by created_at desc
        """, uuid.UUID(device_id))
    return [_row_with_meta(r) for r in rows]


async def get_company_document(doc_id: str, device_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select id::text, device_id::text, filename, mime_type, size_bytes,
                   storage_path, doc_type, link_url, status, visibility,
                   metadata, created_at::text
            from company_documents where id = $1 and device_id = $2
        """, uuid.UUID(doc_id), uuid.UUID(device_id))
    return _row_with_meta(row) if row else None


async def delete_company_document(doc_id: str, device_id: str) -> bool:
    pool = await _get_pool()
    async with pool.acquire() as c:
        n = await c.execute("""
            delete from company_documents where id = $1 and device_id = $2
        """, uuid.UUID(doc_id), uuid.UUID(device_id))
    # n is "DELETE <count>"
    return n.startswith("DELETE ") and not n.endswith(" 0")


async def insert_company_chunk(**fields: Any) -> dict[str, Any]:
    pool = await _get_pool()
    metadata = fields.get("metadata", {})
    emb_lit = _vec_literal(fields["embedding"]) if fields.get("embedding") else None
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into company_chunks(document_id, device_id, page, text,
              token_count, embedding, metadata)
            values ($1, $2, $3, $4, $5, $6::vector, $7::jsonb)
            returning id::text, document_id::text, device_id::text, page,
                      text, metadata, created_at::text
        """, uuid.UUID(fields["document_id"]), uuid.UUID(fields["device_id"]),
             fields.get("page"), fields["text"], fields.get("token_count"),
             emb_lit, json.dumps(metadata))
    out = _row_with_meta(row)
    out["embedding"] = fields.get("embedding")
    return out


async def list_company_chunks(device_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, document_id::text, device_id::text, page, text,
                   embedding::text as embedding_text, metadata, created_at::text
            from company_chunks where device_id = $1
        """, uuid.UUID(device_id))
    out = []
    for r in rows:
        d = _row_with_meta(r)
        emb = d.pop("embedding_text", None)
        d["embedding"] = _parse_vec(emb) if emb else None
        out.append(d)
    return out


# ---------- Artifacts ----------

async def insert_artifact(**fields: Any) -> dict[str, Any]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            insert into generated_artifacts(device_id, conversation_id,
              artifact_type, title, body_md, inputs, citations, status)
            values ($1, $2, $3, $4, $5, $6::jsonb, $7::jsonb, $8)
            returning id::text, device_id::text, conversation_id::text,
                      artifact_type, title, body_md, inputs, citations,
                      status, created_at::text
        """, uuid.UUID(fields["device_id"]),
             uuid.UUID(fields["conversation_id"]) if fields.get("conversation_id") else None,
             fields["artifact_type"], fields["title"], fields["body_md"],
             json.dumps(fields.get("inputs", {})),
             json.dumps(fields.get("citations", [])),
             fields.get("status", "final"))
    return _row_with_meta(row)


async def list_artifacts(device_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id::text, device_id::text, conversation_id::text,
                   artifact_type, title, body_md, inputs, citations,
                   status, created_at::text
            from generated_artifacts where device_id = $1
            order by created_at desc
        """, uuid.UUID(device_id))
    return [_row_with_meta(r) for r in rows]


async def get_artifact(artifact_id: str, device_id: str) -> dict[str, Any] | None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        row = await c.fetchrow("""
            select id::text, device_id::text, conversation_id::text,
                   artifact_type, title, body_md, inputs, citations,
                   status, created_at::text
            from generated_artifacts where id = $1 and device_id = $2
        """, uuid.UUID(artifact_id), uuid.UUID(device_id))
    return _row_with_meta(row) if row else None


# ---------- Audit ----------

async def audit(event_type: str, *, device_id: str | None = None,
                  conversation_id: str | None = None,
                  payload: dict[str, Any] | None = None) -> None:
    pool = await _get_pool()
    async with pool.acquire() as c:
        await c.execute("""
            insert into audit_events(device_id, conversation_id, event_type, payload)
            values ($1, $2, $3, $4::jsonb)
        """,
        uuid.UUID(device_id) if device_id else None,
        uuid.UUID(conversation_id) if conversation_id else None,
        event_type, json.dumps(payload or {}))


async def audit_events_for(device_id: str) -> list[dict[str, Any]]:
    pool = await _get_pool()
    async with pool.acquire() as c:
        rows = await c.fetch("""
            select id, device_id::text, conversation_id::text, event_type,
                   payload, created_at::text
            from audit_events where device_id = $1 order by created_at desc
        """, uuid.UUID(device_id))
    return [dict(r) for r in rows]


def reset_for_tests() -> None:
    """No-op for the live Postgres backend — tests should use the in-memory store."""
    pass
