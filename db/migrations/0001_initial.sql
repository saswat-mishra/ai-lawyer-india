-- AI Lawyer India - Initial Supabase / Postgres schema
-- Requires: pgvector extension. Run on Supabase or local Postgres 15+.

create extension if not exists vector;
create extension if not exists pg_trgm;
create extension if not exists "uuid-ossp";

-- ============================================================
-- Sessions and conversations (device-ID scoped, no auth)
-- ============================================================

create table if not exists devices (
  device_id uuid primary key default uuid_generate_v4(),
  persona text not null default 'citizen' check (persona in ('citizen','founder','practitioner')),
  language_pref text not null default 'en',  -- 'en','hi','en+hi','mr','ta', etc.
  created_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now()
);

create index if not exists idx_devices_last_seen on devices (last_seen_at desc);

create table if not exists conversations (
  id uuid primary key default uuid_generate_v4(),
  device_id uuid not null references devices(device_id) on delete cascade,
  title text,
  workflow text,                         -- 'chat' | 'draft:rental' | 'notice:s138' | ...
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_conversations_device on conversations (device_id, updated_at desc);

create table if not exists messages (
  id uuid primary key default uuid_generate_v4(),
  conversation_id uuid not null references conversations(id) on delete cascade,
  role text not null check (role in ('user','assistant','system','clarification')),
  content text not null,
  -- Structured payloads (citations, decomposition steps, retrieved chunk IDs).
  meta jsonb not null default '{}'::jsonb,
  confidence text check (confidence in ('high','medium','low','refused')),
  created_at timestamptz not null default now()
);

create index if not exists idx_messages_conversation on messages (conversation_id, created_at);

-- ============================================================
-- Legal corpus (shared across all devices)
-- ============================================================

create table if not exists legal_documents (
  id uuid primary key default uuid_generate_v4(),
  source_type text not null check (source_type in (
    'constitution','central_statute','state_statute','rules',
    'case','circular','treatise','bare_act_amendment'
  )),
  jurisdiction text not null default 'india',  -- 'india' or state code 'MH','DL','KA'...
  title text not null,
  short_citation text,                          -- e.g. 'BNS', 'AIR 1986 SC 180'
  long_citation text,
  effective_from date,
  effective_to date,                            -- null = currently in force
  status text not null default 'in_force' check (status in (
    'in_force','repealed','amended','stayed','overruled','doubted','distinguished'
  )),
  source_url text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_legal_docs_source_type on legal_documents (source_type);
create index if not exists idx_legal_docs_jurisdiction on legal_documents (jurisdiction);
create index if not exists idx_legal_docs_status on legal_documents (status);

-- Each chunk is a structurally meaningful unit (Section, Article, Headnote, Held, etc.).
create table if not exists legal_chunks (
  id uuid primary key default uuid_generate_v4(),
  document_id uuid not null references legal_documents(id) on delete cascade,
  hierarchy_path text[] not null,        -- ['Constitution','Part III','Art. 21']
  chunk_type text not null,              -- 'section','article','clause','headnote','facts','issues','held','ratio','obiter'
  section_number text,                   -- normalised key for lookups: '103', '21', '420'
  text text not null,
  token_count int,
  -- Cross-statute mapping (IPC -> BNS, etc.)
  successor_chunk_id uuid references legal_chunks(id) on delete set null,
  predecessor_chunk_id uuid references legal_chunks(id) on delete set null,
  -- Vector for semantic retrieval. Dim must match OPENAI_EMBEDDING_DIM (1536 default).
  embedding vector(1536),
  -- Lexical search column.
  tsv tsvector,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- Vector index. ivfflat is fine for moderate scale. Switch to hnsw on Postgres >= 16
-- for better recall at cost of build time.
create index if not exists idx_legal_chunks_embedding
  on legal_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100);

create index if not exists idx_legal_chunks_tsv on legal_chunks using gin (tsv);
create index if not exists idx_legal_chunks_section on legal_chunks (section_number);
create index if not exists idx_legal_chunks_document on legal_chunks (document_id);
create index if not exists idx_legal_chunks_type on legal_chunks (chunk_type);

-- Trigger to keep tsvector up to date.
create or replace function legal_chunks_tsv_update() returns trigger as $$
begin
  new.tsv := setweight(to_tsvector('simple', coalesce(new.section_number,'')), 'A')
          || setweight(to_tsvector('simple', coalesce(new.text,'')), 'B');
  return new;
end
$$ language plpgsql;

drop trigger if exists trg_legal_chunks_tsv on legal_chunks;
create trigger trg_legal_chunks_tsv before insert or update of text, section_number
on legal_chunks for each row execute function legal_chunks_tsv_update();

-- IPC <-> BNS section mapping (and other transition tables).
-- This is the single feature that beats most general LLMs today.
create table if not exists statute_section_mapping (
  id uuid primary key default uuid_generate_v4(),
  old_act text not null,                 -- 'IPC','CrPC','Indian Evidence Act'
  old_section text not null,
  new_act text not null,                 -- 'BNS','BNSS','BSA'
  new_section text not null,
  effective_from date not null default '2024-07-01',
  notes text,
  unique (old_act, old_section, new_act, new_section)
);

-- Citator graph (case A cites case B, with treatment label).
create table if not exists case_citations (
  id bigserial primary key,
  source_doc_id uuid not null references legal_documents(id) on delete cascade,
  cited_doc_id uuid not null references legal_documents(id) on delete cascade,
  treatment text check (treatment in ('followed','distinguished','doubted','overruled','referred')),
  paragraph int,
  unique (source_doc_id, cited_doc_id, paragraph)
);

create index if not exists idx_case_citations_cited on case_citations (cited_doc_id);

-- ============================================================
-- Per-device company knowledge base
-- ============================================================

create table if not exists company_documents (
  id uuid primary key default uuid_generate_v4(),
  device_id uuid not null references devices(device_id) on delete cascade,
  filename text not null,
  mime_type text not null,
  size_bytes bigint not null,
  storage_path text,                     -- key in Supabase Storage
  status text not null default 'uploaded' check (status in (
    'uploaded','processing','ready','failed'
  )),
  doc_type text,                         -- 'agreement','policy','logo','image','link','note'
  link_url text,                         -- if doc_type='link'
  visibility text not null default 'private' check (visibility in ('private')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_company_docs_device on company_documents (device_id, created_at desc);

create table if not exists company_chunks (
  id uuid primary key default uuid_generate_v4(),
  document_id uuid not null references company_documents(id) on delete cascade,
  device_id uuid not null,               -- denormalised for fast namespace filter
  page int,
  text text not null,
  token_count int,
  embedding vector(1536),
  tsv tsvector,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_company_chunks_embedding
  on company_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 50);

create index if not exists idx_company_chunks_device on company_chunks (device_id);
create index if not exists idx_company_chunks_tsv on company_chunks using gin (tsv);

create or replace function company_chunks_tsv_update() returns trigger as $$
begin
  new.tsv := to_tsvector('simple', coalesce(new.text,''));
  return new;
end
$$ language plpgsql;

drop trigger if exists trg_company_chunks_tsv on company_chunks;
create trigger trg_company_chunks_tsv before insert or update of text
on company_chunks for each row execute function company_chunks_tsv_update();

-- ============================================================
-- Outputs persisted: drafts, notices, opinions
-- ============================================================

create table if not exists generated_artifacts (
  id uuid primary key default uuid_generate_v4(),
  device_id uuid not null references devices(device_id) on delete cascade,
  conversation_id uuid references conversations(id) on delete set null,
  artifact_type text not null,           -- 'draft:rental','notice:s138','opinion','strategy_memo'
  title text not null,
  body_md text not null,
  inputs jsonb not null default '{}'::jsonb,
  citations jsonb not null default '[]'::jsonb,
  status text not null default 'final',
  created_at timestamptz not null default now()
);

create index if not exists idx_artifacts_device on generated_artifacts (device_id, created_at desc);

-- ============================================================
-- Audit and eval
-- ============================================================

create table if not exists audit_events (
  id bigserial primary key,
  device_id uuid,
  conversation_id uuid,
  event_type text not null,              -- 'retrieval','synthesis','verification','refusal','web_search','company_kb_use'
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_audit_device on audit_events (device_id, created_at desc);
create index if not exists idx_audit_event_type on audit_events (event_type);

-- ============================================================
-- Helper views
-- ============================================================

create or replace view good_law_cases as
  select * from legal_documents
  where source_type = 'case'
    and status not in ('overruled','doubted')
    and (effective_to is null or effective_to > now());

-- Hybrid retrieval helper: caller passes in query embedding and a tsquery.
-- Returns chunks scored by cosine similarity AND lexical rank.
create or replace function hybrid_search_legal(
  q_embedding vector(1536),
  q_tsquery tsquery,
  k int default 50
) returns table (
  chunk_id uuid,
  document_id uuid,
  text text,
  hierarchy_path text[],
  chunk_type text,
  section_number text,
  cosine_sim float,
  lexical_rank float
) as $$
  select c.id, c.document_id, c.text, c.hierarchy_path, c.chunk_type, c.section_number,
         1 - (c.embedding <=> q_embedding) as cosine_sim,
         ts_rank_cd(c.tsv, q_tsquery) as lexical_rank
  from legal_chunks c
  join legal_documents d on d.id = c.document_id
  where d.status not in ('overruled','doubted')
  order by (1 - (c.embedding <=> q_embedding)) * 0.6
         + ts_rank_cd(c.tsv, q_tsquery) * 0.4 desc
  limit k;
$$ language sql stable;

create or replace function hybrid_search_company(
  p_device_id uuid,
  q_embedding vector(1536),
  q_tsquery tsquery,
  k int default 30
) returns table (
  chunk_id uuid,
  document_id uuid,
  text text,
  cosine_sim float,
  lexical_rank float
) as $$
  select c.id, c.document_id, c.text,
         1 - (c.embedding <=> q_embedding) as cosine_sim,
         ts_rank_cd(c.tsv, q_tsquery) as lexical_rank
  from company_chunks c
  where c.device_id = p_device_id
  order by (1 - (c.embedding <=> q_embedding)) * 0.6
         + ts_rank_cd(c.tsv, q_tsquery) * 0.4 desc
  limit k;
$$ language sql stable;

-- Touch updated_at on conversations when messages added.
create or replace function touch_conversation() returns trigger as $$
begin
  update conversations set updated_at = now() where id = new.conversation_id;
  return new;
end
$$ language plpgsql;

drop trigger if exists trg_touch_conv on messages;
create trigger trg_touch_conv after insert on messages
for each row execute function touch_conversation();
