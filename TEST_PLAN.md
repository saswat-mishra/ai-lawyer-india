# AI Lawyer India — Test Plan

This is the contract: a build is "done" when every test in this plan that does *not* require an OpenAI API key passes. After the user adds the key, the OpenAI-gated tests must also pass.

## 0. Test infrastructure

- **Backend Python**: `pytest`, `pytest-asyncio`, `httpx` (for API tests), `respx` (HTTP mocking), `freezegun`.
- **Frontend Next.js**: `vitest` + `@testing-library/react` for component tests, `playwright` for E2E.
- **Cross-cutting**: a custom **citation faithfulness harness** in `tests/integration/citation_harness.py`.
- **CI runner**: `make test-no-key` runs every gate that does not need OpenAI; `make test-with-key` runs full suite.

Markers:
- `@pytest.mark.openai` — requires `OPENAI_API_KEY`.
- `@pytest.mark.live` — requires network (web search, scrapers).
- `@pytest.mark.slow` — > 2s.

`make test-no-key` excludes `openai` and `live`.

## 1. Backend — unit tests

### 1.1 Config and env loading (`tests/unit/test_config.py`)
- Defaults are sane when env vars unset.
- Model identifiers parse correctly.
- pgvector connection string composition is correct.
- Persona enum has Citizen/Founder/Practitioner.

### 1.2 Device ID handling (`tests/unit/test_device_id.py`)
- New device gets a UUID v4 cookie.
- Existing device cookie is preserved.
- Cookie signing rejects tampering.
- Cookie expiry is 1 year from set time.

### 1.3 Chunker (`tests/unit/test_chunker.py`)
- Statute chunking respects Section boundaries (no cross-section bleed).
- Proviso/Explanation are linked to parent Section, never orphaned.
- Case chunker isolates Headnote / Held / Ratio.
- Long sections split on subsection but never on word.
- Returns valid `Chunk` objects with hierarchy_path populated.

### 1.4 Citation parser (`tests/unit/test_citations.py`)
- Parses "Section 103 BNS", "S. 103, BNS", "section 103 of the Bharatiya Nyaya Sanhita, 2023".
- Parses "Olga Tellis v. Bombay Municipal Corporation, AIR 1986 SC 180".
- Parses "(2017) 4 SCC 312".
- Rejects malformed citations.
- IPC↔BNS mapping table loads correctly and `successor_section` resolves.

### 1.5 Citation verifier (`tests/unit/test_citation_verifier.py`)
- A claim citing a section that exists in the corpus index passes.
- A claim citing a fake section is flagged.
- Quoted text that doesn't appear verbatim in the source is flagged.
- Existence check is case-insensitive on case names.
- Verifier produces a structured failure report.

### 1.6 RAG pipeline assembly (`tests/unit/test_rag.py`)
- Dense retrieval returns chunks ordered by cosine similarity (mocked embeddings).
- Lexical retrieval honors `tsvector` weights.
- Reciprocal Rank Fusion produces deterministic ordering.
- Status filter excludes overruled cases.
- Persona-aware retrieval: Citizen mode caps results at 6, Practitioner at 20.

### 1.7 Company KB ingestion (`tests/unit/test_company_kb.py`)
- PDF text extraction (sample 3-page PDF in `tests/fixtures/`).
- DOCX extraction (sample).
- Plaintext / markdown.
- Image OCR fallback (skipped if tesseract not installed).
- Chunks are written with `device_id` namespace and never visible across devices.

### 1.8 Clarification agent (`tests/unit/test_clarifier.py`)
- "My landlord is evicting me" → asks for state + tenancy type.
- "Can I sue Acme Corp for breach?" → asks for jurisdiction + facts of breach.
- All required slots filled → no questions, returns `ready=True`.
- Never asks more than 3 questions in one turn.

### 1.9 Web search tool (`tests/unit/test_web_search.py`)
- Tool dispatches to Tavily/SerpAPI driver based on env.
- Falls back to "no results" gracefully when driver unset.
- Caches identical queries within session.

## 2. Backend — API tests (`tests/api/`)

Run a real FastAPI test client. No external services.

- `POST /api/session` — issues device ID cookie if missing; returns persona = Citizen by default.
- `PATCH /api/session/persona` — updates persona to founder; persists.
- `POST /api/chat` — accepts a query; with a stubbed agent, returns SSE stream chunks.
- `GET /api/chat/{conversation_id}` — returns conversation with messages and source attributions.
- `POST /api/company/docs` — accepts upload; stores in fixture storage; returns ingestion status.
- `GET /api/company/docs` — lists docs for current device only (cross-device isolation test).
- `DELETE /api/company/docs/{id}` — removes doc and deletes its chunks.
- `POST /api/draft` — given workflow `rental_agreement` and inputs, returns a draft (with stubbed model, deterministic output).
- `POST /api/notice` — given workflow `s138_ni_act_notice` and inputs, returns a notice.
- `GET /api/sources/{citation_id}` — returns source paragraph and metadata.
- 404, 422, 500 paths.

## 3. Backend — RAG and agent integration tests (`tests/integration/`)

Use a small in-process corpus of known sections + 3 case headnotes (fixtures).

- **Retrieval recall**: 50 hand-written queries → expected top-1 chunk; recall@5 ≥ 0.85.
- **Citation faithfulness**: 30 queries through the agent (with stubbed LLM that emits both real and fake citations) → verifier strips 100% of fakes.
- **No leakage between devices**: device A uploads a confidential doc; device B's chat must never retrieve it.
- **Status filter**: an overruled case in the index is *not* surfaced as good law unless the question is explicitly about its overruling.
- **Persona depth**: same query under Citizen vs Practitioner produces materially different output structure (asserted via output schema).
- **Refusal floor**: a query with no good retrieval support returns a refusal with the exact phrase "I couldn't find authoritative basis".

## 4. Frontend — unit & component tests

- `<DeviceProvider>` issues an ID, persists, and resolves on mount.
- `<PersonaSwitcher>` updates session and refetches workflows.
- `<CitationPill>` opens the source drawer with correct content on click.
- `<ConfidenceBadge>` renders correct color for High/Medium/Low/Refused.
- `<DraftEditor>` clause-level annotations render and respond to right-click "explain this".
- `<CompanyDocUploader>` shows progress; rejects > 50MB; refuses non-allowed mime.
- `<ChatMessage>` renders streamed deltas without flicker.

## 5. Frontend — E2E (Playwright)

Run against `next dev` + a stubbed backend (separate `pytest`-launched test server with deterministic fixtures).

- **First-run flow**: visit landing → select persona → land on chat → ask question → see streamed answer with citations → click citation → drawer opens → reload page → conversation persisted via device ID.
- **Drafting flow**: persona = Founder → workflow picker → rental agreement → fill 6 inputs → preview → download as DOCX → file integrity check.
- **Company KB flow**: upload a PDF → see processing state → ask a question that requires it → answer cites company doc with the right tag.
- **Clarification flow**: ask underspecified question → see clarifying questions appear with choices → answer → final answer arrives.
- **Cross-device isolation**: open two browser contexts, upload doc in context A, query in context B → company doc not referenced.
- **Mobile viewport**: chat surface adapts; citation drawer is full-screen sheet.

## 6. Citation faithfulness harness

The keystone test. Lives in `tests/integration/citation_harness.py`.

For each entry in `tests/fixtures/citation_eval.jsonl`:
- Run the full agent end-to-end (with mocked OpenAI returning a *deterministic, deliberately-mixed* output: 70% real citations, 30% fabricated).
- Verify: every citation in the *final user-facing output* exists in the corpus.
- Verify: every quoted sentence appears in the cited source.
- Fail the build if a fabricated citation survives.

The fabricated-citation insertion is what makes this brutal — it forces the verifier to actually do its job.

## 7. Performance gates

- p95 retrieval latency < 800ms over a 10k-chunk corpus on a laptop.
- p95 first-token-from-stream < 2s when LLM is mocked.
- Frontend Lighthouse: Performance ≥ 85, Accessibility ≥ 95.
- No memory leak across 100 chat turns (assert RSS stable within 5%).

## 8. Resilience

- Backend kills mid-stream → frontend shows reconnect UI and retries.
- Vector DB down → retrieval returns "service degraded" instead of crashing.
- OpenAI rate-limit → exponential backoff with jitter, surfaced to UI as "slowed down".
- Malformed user input (binary in chat) → rejected with 422.

## 9. Security

- Cookie tampering → reject with 400.
- Path traversal in file upload filenames → sanitised.
- SQL injection in chat query → parameterised everywhere; `bandit` static check.
- File upload virus scan placeholder (interface ready, scanner pluggable).
- CORS locked to known origins in prod, open in dev.

## 10. Accessibility (WCAG AA)

- All interactive elements keyboard-reachable.
- Color contrast ratio ≥ 4.5:1 for body text.
- Citation pills have ARIA labels.
- Drawer is focus-trapped when open.
- Screen-reader announce on persona change and confidence-badge appearance.

## 11. The "make test-no-key" gate

Implemented as `Makefile` target. Runs:
1. Python lint (`ruff`, `black --check`).
2. Type check (`mypy app`).
3. `pytest -m "not openai and not live"`.
4. Frontend `pnpm lint && pnpm typecheck && pnpm vitest run`.
5. Playwright headless E2E with backend stubbed.
6. Citation faithfulness harness (uses fixed mocked LLM outputs, no API needed).

This gate is what runs end-to-end before declaring "COMPLETED".

## 12. The "make test-with-key" gate

Adds:
- Live OpenAI calls against a 20-question gold set; check answer existence + citation faithfulness on real outputs.
- Real embedding generation; recall@5 against gold.
- Cost ceiling: total spend on the gate < ₹100 worth of tokens.

