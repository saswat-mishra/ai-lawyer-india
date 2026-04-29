# Run the project

## Prereqs
- Python 3.10+ (3.11 recommended)
- Node 18+ + pnpm (or npm)
- Postgres 15+ with pgvector (or use Docker — see below)

## 1. Add OpenAI key

```bash
cp .env.example .env
# edit .env, set OPENAI_API_KEY=sk-...
```

## 2. Backend

```bash
cd backend
pip install -e ".[dev]"
# In-memory mode (no Postgres needed for first boot):
AIL_FORCE_MEMORY=1 uvicorn app.main:app --reload --port 8000
```

The server seeds a working corpus on boot (BNS, IPC, NI Act, Contract Act, TP Act,
Constitution, leading cases). Health check:

```bash
curl http://localhost:8000/api/health
# {"ok":true,"has_openai":true,"env":"development"}
```

## 3. Frontend

```bash
cd frontend
pnpm install      # or: npm install
pnpm dev
# open http://localhost:3000
```

## 4. (Optional) Real Postgres + bigger corpus

```bash
docker compose up -d db
psql "postgresql://postgres:postgres@localhost:54322/postgres" \
  -f db/migrations/0001_initial.sql \
  -f db/migrations/0002_seed_mappings.sql

# Now run scrapers:
AIL_FORCE_PG=1 python -m scripts.scrape_indiacode --acts BNS,NI_Act,ContractAct,TPAct,CPA
AIL_FORCE_PG=1 python -m scripts.scrape_states --states MH,DL,KA
AIL_FORCE_PG=1 python -m scripts.scrape_sci --year 2024 --max 50
```

## 5. Tests

```bash
# No API key, no network — runs in 1 second
make test-no-key

# With key
make test-with-key
```

## 6. End-to-end smoke test (manual)

1. Open http://localhost:3000
2. Click a starter prompt (e.g., "What is Section 103 BNS?")
3. Answer streams in with citation pills
4. Click a pill — drawer shows the source paragraph
5. Switch persona (Citizen → Practitioner) in the sidebar
6. Same question now produces practitioner-grade prose
7. Open Company KB → drop a PDF → ask a question that mentions the doc → answer cites it
