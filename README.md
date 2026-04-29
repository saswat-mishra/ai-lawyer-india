# AI Lawyer India

India-first AI lawyer. Citation-faithful, BNS/BNSS/BSA-current, persona-tailored, with a per-device company knowledge base.

## Quickstart

```bash
# 1. Boot Postgres + pgvector
docker compose up -d db

# 2. Apply migrations
psql "$DATABASE_URL" -f db/migrations/0001_initial.sql

# 3. Backend
cd backend
uv sync     # or: pip install -e .
cp ../.env.example .env
uvicorn app.main:app --reload --port 8000

# 4. Frontend (separate terminal)
cd frontend
pnpm install
pnpm dev

# 5. Seed corpus (after OPENAI_API_KEY is set)
cd backend
python -m scripts.ingest_seed_corpus
```

## Test gates

```bash
# No API key required
make test-no-key

# With OPENAI_API_KEY set
make test-with-key
```

## Directories

- `frontend/` — Next.js 14 App Router.
- `backend/` — FastAPI, LangGraph agent, RAG.
- `db/migrations/` — Supabase Postgres SQL.
- `corpus/` — downloaded raw legal documents (gitignored).
- `scripts/` — scrapers and ingestion.
- `tests/integration/` — full-stack tests.

See `knowledge.md` for full design rationale and `TEST_PLAN.md` for the test contract.
