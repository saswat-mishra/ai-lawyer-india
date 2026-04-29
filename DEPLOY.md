# Deployment

## What's already done (this session)

| Service | Status | Notes |
|---|---|---|
| Supabase project | ✅ created | `ai-lawyer-india` in `ap-south-1` (Mumbai), id `dcqvznagpsouslkaqlct` |
| Schema | ✅ applied | `0001_initial_schema` + `0002_seed_ipc_bns_mapping` |
| Project URL | ✅ | `https://dcqvznagpsouslkaqlct.supabase.co` |
| Publishable anon key | ✅ | (in your Supabase dashboard) |
| `.gitignore` | ✅ written | `.env` excluded |
| `vercel.json` | ✅ written | Next.js + Python serverless under `/api` |
| `api/index.py` | ✅ written | ASGI entrypoint exposing `app.main:app` |
| `requirements.txt` | ✅ written | Pinned Python deps for the serverless function |
| `frontend/next.config.js` | ✅ updated | No-op rewrite in prod (Vercel routes `/api/*` natively) |

## What still requires you (auth boundaries)

The Vercel and GitHub MCPs in this session can't OAuth on your behalf —
you need to run two CLI commands.

### 1. Push to GitHub

```bash
cd /Users/saswat/.../outputs/ai-lawyer-india

git init -b main
git add -A
git commit -m "AI Lawyer India: initial deploy"

# Option A: gh CLI (recommended)
gh repo create ai-lawyer-india --private --source=. --push

# Option B: create the repo on github.com first, then:
git remote add origin git@github.com:<your-user>/ai-lawyer-india.git
git push -u origin main
```

### 2. Deploy on Vercel

Two paths:

**A. Connect GitHub (most native)**
1. Go to [vercel.com/new](https://vercel.com/new).
2. Import the `ai-lawyer-india` repo.
3. **Framework preset**: Next.js will be auto-detected.
4. **Root directory**: leave at repo root (we've configured `vercel.json` to
   build `frontend/` and route Python under `/api`).
5. **Environment variables**: paste the table below.
6. Click **Deploy**. First build is ~3–5 minutes.

**B. CLI**
```bash
npm i -g vercel
vercel login
cd /Users/saswat/.../outputs/ai-lawyer-india
vercel --prod
```
The CLI will read `vercel.json` and prompt you to add env vars.

## Required Vercel environment variables

Copy these into Vercel → Project → Settings → Environment Variables.

| Name | Value | Scope |
|---|---|---|
| `OPENAI_API_KEY` | `sk-proj-...` (your key) | Production + Preview |
| `OPENAI_MODEL_DEFAULT` | `gpt-4o-mini` | Production + Preview |
| `OPENAI_MODEL_HEAVY` | `gpt-4o` | Production + Preview |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Production + Preview |
| `OPENAI_EMBEDDING_DIM` | `1536` | Production + Preview |
| `SUPABASE_URL` | `https://dcqvznagpsouslkaqlct.supabase.co` | Production + Preview |
| `SUPABASE_ANON_KEY` | (publishable key from Supabase dashboard) | Production + Preview |
| `DATABASE_URL` | `postgresql://postgres:<DB_PASSWORD>@db.dcqvznagpsouslkaqlct.supabase.co:5432/postgres` | Production + Preview |
| `DEVICE_COOKIE_SECRET` | a long random string (32+ chars) | Production + Preview |
| `ALLOWED_ORIGINS` | `https://<your-vercel-domain>.vercel.app` | Production + Preview |
| `APP_ENV` | `production` | Production |
| `AIL_FORCE_MEMORY` | `1` (temporary — see note below) | Production + Preview |

> **Note on `AIL_FORCE_MEMORY=1`:** the current backend uses an in-memory
> store. On Vercel each function invocation is a fresh container, so device
> sessions and conversations won't persist across requests. This is fine for
> kicking the tyres on the live deployment, but for real production use the
> backend needs to be wired to Supabase Postgres. See
> "Postgres backend follow-up" below.

## Postgres backend follow-up

`app/db/store.py` is currently in-memory. To make the cloud deployment
stateful:

1. Add an `app/db/pg_store.py` (asyncpg-based, mirroring the same
   surface that `app/db/store.py` exposes).
2. In `app/db/__init__.py`, route to `pg_store` when `AIL_FORCE_PG=1` or
   `DATABASE_URL` points at a non-localhost Postgres.
3. Embed every `legal_chunks.embedding` and `company_chunks.embedding` as
   a `vector(1536)` literal: `cast($1 as vector(1536))` with `$1` being a
   `[1.0, 0.4, ...]` string.
4. Replace the Python-side dense-cosine + bm25-ish loops with calls to the
   SQL function `hybrid_search_legal()` (already defined in the migration).
5. Set `AIL_FORCE_PG=1` and remove `AIL_FORCE_MEMORY=1` from Vercel.

This is a clean follow-up issue.

## Smoke tests after deploy

After the deploy lands, run these against the live URL:

```bash
DEPLOY=https://<your-vercel-domain>.vercel.app

# 1. Health
curl $DEPLOY/api/health
# Expect: {"ok":true,"has_openai":true,"env":"production"}

# 2. Session
curl -c /tmp/c.txt -X POST $DEPLOY/api/session
# Expect: {"device_id":"...","persona":"citizen","language_pref":"en"}

# 3. Chat
curl -b /tmp/c.txt -X POST $DEPLOY/api/chat \
  -H 'content-type: application/json' \
  -d '{"query":"What is the punishment for murder under Indian law?"}'
# Expect: streamed answer with citations to Section 103 BNS or 302 IPC.

# 4. Open the frontend in your browser
open $DEPLOY
```
