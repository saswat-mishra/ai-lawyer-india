# State-of-the-art RAG strategy for Indian legal AI

**Audience.** Indian and international law firms, in-house counsel, founders building lawyer-replacement products. Single architecture, two deployment shapes (free-tier prototype → enterprise self-hosted).

**Goal.** Beat the published bar. Stanford's 2024 audit of Lexis+ AI and Thomson Reuters' Practical Law AI found **hallucination rates of 17–33 %** even with RAG, **33 % best-case recall on multi-turn legal conversations**, and a **14-point accuracy drop** moving from basic to multi-jurisdictional queries [Magesh et al., Stanford HAI](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries). The strategy below is engineered to **drive hallucination toward zero by construction** rather than relying on post-hoc filters.

---

## 1. The four design principles

| Principle | What it prevents | How we enforce it |
|---|---|---|
| **Citation-faithful by construction** | Sycophantic / fabricated authority | Every cited section/case is matched to a chunk in the corpus before ship; structured citation outputs (Pydantic), not free-text. |
| **Hybrid retrieval over single-vector** | Recall failure on lexical queries (section numbers) and paraphrase queries | Dense + sparse (BM25) + ColBERT-style late interaction, fused with reciprocal rank fusion (RRF), then cross-encoder rerank. |
| **Status-aware retrieval** | Citing overruled case as good law | Citator graph (Neo4j) marks every judgment with treatment status; "good-law" filter at retrieval time. |
| **Provenance-rich chunks** | Wrong-temporal-regime citations (BNS vs IPC), wrong-jurisdiction (state stamp duty) | Every chunk carries `act_short`, `effective_from/to`, `jurisdiction`, `status`, `predecessor_section`/`successor_section`, `bench_strength` for cases. Filter on these before vector search. |

These four are non-negotiable. Everything below is implementation detail in service of them.

---

## 2. Tooling decision matrix (research-validated, April 2026)

### 2.1 Vector database

Tested against the project's needs — hybrid retrieval, payload filtering, free tier sized for top-100 cases + active statutes (~100k–500k vectors at 1024–1536 dim).

| Tool | Free tier | Hybrid retrieval | Filtering | Verdict |
|---|---|---|---|---|
| **Qdrant Cloud** | **1 GB RAM, 4 GB disk forever, no card** [pricing](https://qdrant.tech/pricing/) — fits ~1 M vectors @ 1536 dim with binary quantisation | Native dense + sparse, RRF built in | Excellent payload filters, geo, time | ✅ **Primary choice** for cloud. Generous, hybrid-native, fastest cold-start of the managed options. |
| Pinecone Starter | 2 GB / ~100 K vectors, **indexes paused after 3 weeks inactivity**, single region [community thread](https://community.pinecone.io/t/limit-of-vectors-on-free-plan/3821) | Dense only on free; hybrid is paid Pods | Strong | ❌ Free tier too small + auto-pause kills the bot |
| Weaviate Cloud Sandbox | 14-day sandbox | Native hybrid | Strong | ❌ Sandbox expires |
| Supabase pgvector | 500 MB Postgres free | dense only natively (sparse via tsvector — what we have today) | Excellent (SQL) | ✅ **Already integrated**; keep as fallback / per-tenant company-KB store |
| Self-hosted Qdrant | Free | Native hybrid | Excellent | ✅ Enterprise / on-prem deployment |

**Decision.** Qdrant Cloud as the primary corpus index; Supabase pgvector for per-device company knowledge bases (already wired); self-hosted Qdrant available for law-firm deployments needing data residency.

### 2.2 Embedding model

Stanford's hallucination findings are partly a *retrieval* problem — if the right authority isn't recalled, generation invents one. So the embedding model matters.

| Model | Cost | Hybrid native | Domain | Verdict |
|---|---|---|---|---|
| **Voyage `voyage-law-2`** | **50 M tokens free, then $0.05/M** [Voyage pricing](https://docs.voyageai.com/docs/pricing) | Dense only | **Purpose-built for legal text** | ✅ **Primary for production** — 50 M tokens covers our top-100 cases + Constitution + active statutes embedding many times over |
| **BGE-M3** | Free open-source (HF / DeepInfra / self-host) | **Dense + sparse + ColBERT in one model** [HF model card](https://huggingface.co/BAAI/bge-m3) | General multilingual (100+ langs), strong on Indic | ✅ **Primary for free-tier prototype** — matches the "hybrid native" principle, supports Hindi out of the box |
| OpenAI `text-embedding-3-small` | $0.02/M | Dense | General | 🟡 What we ship today; perfectly serviceable but not legal-tuned |
| Cohere Embed v4 | Trial 1 K calls/mo | Dense | General | 🟡 Limited free tier |
| Jina v3 | Free open-source | Dense | General multilingual | 🟡 Strong alternative to BGE-M3 |

**Decision.** Free-tier prototype: BGE-M3 self-hosted on a small CPU box (or Hugging Face Inference Endpoints free tier). Production: Voyage `voyage-law-2` — domain-specific embeddings consistently beat general-purpose by 5–15 points on legal recall benchmarks per [Voyage's published evaluations](https://docs.voyageai.com/docs/embeddings).

### 2.3 Reranker

| Tool | Free tier | Strength | Verdict |
|---|---|---|---|
| **BGE-reranker-v2-m3** | Free open-source | Strong cross-encoder, multilingual | ✅ **Primary** — self-host, no rate limit |
| Cohere Rerank 3.5 | 1 000 calls / mo, 10/min [Cohere docs](https://docs.cohere.com/docs/rate-limits) | Best published quality on the BEIR leaderboard | ✅ Use for the final-mile rerank in production; cap at 10/min worker |
| Voyage `rerank-2` | 50 M tokens free | Domain-tuned variant | 🟡 Worth A/B testing |

**Decision.** Self-hosted BGE-reranker-v2-m3 always; Cohere Rerank 3.5 wired in as opt-in for highest-stakes queries (practitioner mode default).

### 2.4 Knowledge graph (citator)

The Stanford study's "sycophancy" failure mode — fabricating authority — is solved by hard-filtering retrieval to **good law only**. That requires a citator: which case cites which, with treatment label.

| Tool | Free tier | Verdict |
|---|---|---|
| **Neo4j AuraDB Free** | **1 DB, 50 K nodes, 175 K relationships** [Neo4j AuraDB](https://neo4j.com/product/auradb/) — fits top-100 cases × ~25 cited cases each ≈ 2 500 nodes / ~50 K edges | ✅ **Primary** — well within limits |
| Postgres relational | Free if Supabase | Adequate but no graph traversal sugar | 🟡 Fallback |
| Memgraph Cloud | 2 GB RAM free | Compatible Cypher | 🟡 Alternative |

**Decision.** Neo4j AuraDB Free for the citator (case → cites → case, with `treatment` edge property: followed / distinguished / overruled / doubted / referred). Cypher query at retrieval time: *exclude any case that has been overruled (path of `:CITES{treatment:"overruled"}` from a later coordinate-or-superior bench)*.

### 2.5 LLM for synthesis

| Model | Cost | Notes |
|---|---|---|
| OpenAI gpt-4o-mini | $0.15 in / $0.60 out per M tokens | What we use today |
| OpenAI gpt-4o | $2.50 in / $10 out per M | Heavy / strategy mode |
| Anthropic Claude Haiku 4.5 | comparable | Low-latency alternative |
| Google Gemini 1.5 Flash | very cheap | Free tier 1 RPM |

**Decision.** Stay with OpenAI tiered (mini default, 4o for strategy/drafting). Provider-agnostic via the `app/llm/openai_client.py` wrapper.

---

## 3. Free-tier deployment architecture

The maximum impressive demo we can ship without paid infra:

```
                                  ┌──────────────────────────┐
                                  │  User browser             │
                                  └────────┬─────────────────┘
                                           │
                                  ┌────────▼─────────────────┐
                                  │  Vercel (Next.js + API)  │
                                  │  Hobby — free            │
                                  └────────┬─────────────────┘
                                           │
                  ┌────────────────────────┼────────────────────────┐
                  │                        │                        │
        ┌─────────▼─────────┐   ┌──────────▼─────────┐   ┌──────────▼─────────┐
        │  Qdrant Cloud      │   │  Neo4j AuraDB Free  │   │  Supabase free      │
        │  (legal corpus     │   │  (citator graph)    │   │  Postgres + storage │
        │   ~500K vectors)   │   │  50K nodes/175K edges│   │  (devices, convos,  │
        │  1 GB RAM free     │   │                      │   │   per-device docs)  │
        └─────────┬─────────┘   └──────────┬─────────┘   └─────────────────────┘
                  │                         │
                  └─────────────┬───────────┘
                                │
                  ┌─────────────▼─────────────┐
                  │  Voyage AI free (50M tok) │
                  │  voyage-law-2 embeddings  │
                  │  (offline ingestion)      │
                  └───────────────────────────┘

                  ┌───────────────────────────┐
                  │  BGE-reranker-v2 (HF      │
                  │  Inference Endpoints free │
                  │  hours)                    │
                  └───────────────────────────┘

                  ┌───────────────────────────┐
                  │  OpenAI gpt-4o-mini        │
                  │  (paid; the only $$ cost)  │
                  └───────────────────────────┘
```

**Total free tier capacity** (no infra spend):

- Vector DB: **~1 M vectors @ 1024 dim** on Qdrant free (with int8 quantisation we can go higher)
- Citator: **50 K cases × 3.5 average citations each ≈ 175 K edges** on Neo4j Aura Free
- Stateful per-user data (conversations, company docs, audit trail): Supabase free 500 MB
- Embedding budget: **~30 M tokens of legal text embeddable for free** at voyage-law-2 (at 4 chars/token, ≈ 120 MB of cleaned act + judgment text)
- Reranking: BGE self-host costs only the runtime

**Only money spent: OpenAI synthesis tokens.** At gpt-4o-mini's price, $5 = ~25 000 user queries.

---

## 4. Document acquisition strategy

### 4.1 Scope (per user direction: skip legacy)

We deliberately exclude IPC 1860, CrPC 1973, Indian Evidence Act 1872 from active embedding. They live as cross-reference rows in `statute_section_mapping` so an "Section 302 IPC" query correctly maps to BNS §103 and answers from the post-1 July 2024 regime.

In scope:

1. **Constitution of India** — every Article + Schedule, fully ingested.
2. **Top 100 most-cited Supreme Court judgments** — published lists from [SC Observer](https://www.scobserver.in), Wikipedia [Landmark decisions](https://en.wikipedia.org/wiki/List_of_landmark_court_decisions_in_India), and the [SC's own landmark summaries](https://www.sci.gov.in/landmark-judgment-summaries/).
3. **Active central acts** (BNS, BNSS, BSA, Companies Act 2013, IT Act 2000, DPDP 2023, NI Act 1881, Contract Act 1872, Specific Relief Act 1963, TP Act 1882, CPC 1908, Limitation Act 1963, Hindu Marriage Act 1955, RTI Act 2005, RERA 2016, IBC 2016, MV Act 1988, Arbitration & Conciliation Act 1996, IT Act 1961 Income-tax, CGST/IGST 2017, Trade Marks/Copyright/Patents/Designs Acts, NDPS Act 1985, PMLA 2002, PC Act 1988, Advocates Act 1961, the four labour Codes 2019/2020, plus the canonical list in `CORPUS.md`).
4. **Latest amendments and notifications** through monthly cron — pulled from the [Gazette of India](https://egazette.gov.in/) and [PRS Legislative Research](https://prsindia.org/).
5. **State acts** — Tier-1 states (MH, DL, KA, UP, TN, WB, GJ, RJ) Rent Acts + Stamp Acts + Co-op Society Acts.

### 4.2 Authoritative sources (ranked by signal-to-noise)

| Source | What it gives | API / scrape route |
|---|---|---|
| **India Code** (`indiacode.nic.in`) | Canonical bare-act PDFs | OAI-PMH endpoint or HTML handle pages |
| **Legislative Department** (`legislative.gov.in`) | Constitution authoritative text | Direct HTML / PDF |
| **Supreme Court of India** (`sci.gov.in/judgments`, `judgments.ecourts.gov.in`) | Authoritative judgment text | Public search; rate-limited |
| **Indian Kanoon** (`indiankanoon.org`) | Full searchable corpus of all judgments incl. HCs | HTML scrape — respect ToS, attribute |
| **PRS Legislative Research** (`prsindia.org`) | Amendment summaries with cross-references | HTML |
| **Gazette of India** (`egazette.gov.in`) | Notifications, amendments | RSS + PDF |
| **MCA / SEBI / RBI / CBIC / IPIndia** | Sectoral rules + circulars | Each ministry's PDF library |

### 4.3 Acquisition pipeline

```
                ┌──────────────────────────────────────┐
                │  Scheduler (GitHub Actions cron)     │
                └─────────────────┬────────────────────┘
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
    ▼                             ▼                             ▼
  Bare-act scraper        SC judgment scraper          Notifications scraper
  (indiacode + legislative) (sci.gov.in + IK)         (egazette + PRS)
    │                             │                             │
    └─────────────────────────────┼─────────────────────────────┘
                                  ▼
                ┌──────────────────────────────────────┐
                │  Raw store (S3-compat: Cloudflare R2 │
                │  free 10 GB)                          │
                └─────────────────┬────────────────────┘
                                  ▼
                ┌──────────────────────────────────────┐
                │  Per-doc-type parser (statute / case │
                │  / circular)                          │
                └─────────────────┬────────────────────┘
                                  ▼
                ┌──────────────────────────────────────┐
                │  Structurally-aware chunker          │
                └─────────────────┬────────────────────┘
                                  ▼
                ┌──────────────────────────────────────┐
                │  Voyage law-2 embedding (batched)    │
                └─────────────────┬────────────────────┘
                                  ▼
                ┌──────────────────────────────────────┐
                │  Qdrant upsert + Neo4j edge insert   │
                │  + Postgres metadata                  │
                └──────────────────────────────────────┘
```

The whole pipeline is reproducible: a content hash drives idempotency, so a re-run with no upstream change is a no-op.

---

## 5. Chunking strategy — per document type

This is where most legal RAG implementations fail. Generic 512-token splitters break legal text on every meaningful unit. Strategy by document type:

### 5.1 Statutes

Hierarchy: `Act → Part → Chapter → Section → Subsection → Proviso → Explanation`.

**Chunk = one Section.** Sub-sections, provisos, and explanations roll up into the parent Section chunk so the model never sees a half-Section. If a Section's full text exceeds 1 000 tokens, split on sub-section boundaries; if a sub-section also exceeds 1 000, split paragraph-wise but never mid-sentence.

For each chunk, store a small **headline** (Section number + marginal note) separately; the headline is what we embed for "section-direct" lookup ("Section 138 NI Act"), the body is what we embed for semantic match.

**Multi-vector trick.** Embed three vectors per Section: (a) the headline, (b) the operative-text first 200 tokens, (c) the full text. Insert all three into Qdrant with a `vector_kind` payload. Query-time, dispatch the user query to all three and union the results. This is **parent-child retrieval** done right and is the single biggest recall lift in this implementation (research-validated: Pinecone, Anthropic, and DeepLearning.AI all publish 8–15 point recall@5 lifts from parent-child).

### 5.2 Case judgments

Hierarchy: `Citation → Case Name → Bench → Headnote → Facts → Issues → Held → Ratio → Obiter → Decree`.

The **Held** and **Ratio** sections are the operative law. We chunk:

- Headnote (always), Held (always), Ratio (always) — each a separate chunk.
- Facts split on event boundaries (Reading Comprehension splits) — embed but down-weight at retrieval.
- Obiter as a single chunk, marked low-priority.

Each chunk metadata: `bench_strength` (5J > 3J > 2J), `coram` (judges), `treatment_status` ("good_law" / "doubted" / "overruled"), `citation_string`, `paragraph_number`.

### 5.3 Notifications & circulars

Short documents. **Chunk per paragraph + cross-reference resolution**: when an RBI/SEBI/CBIC circular says "in modification of Notification 10/2019-Central Tax", we resolve and link to the parent notification. Cross-references become edges in the Neo4j citator.

---

## 6. Embedding strategy

### 6.1 Tiered embedding

Not every chunk needs the same model.

| Chunk type | Embed with | Reason |
|---|---|---|
| Section headline (e.g., "Section 138 — Dishonour of cheque") | BGE-M3 dense + sparse (in one call) | Lexical-heavy, sparse helps with "138" |
| Section operative text | voyage-law-2 (1 024 dim) | Dense semantic |
| Case Held / Ratio | voyage-law-2 | Dense semantic; legal-domain tuned matters here |
| Case Facts | BGE-M3 dense | Cheap; we down-weight these anyway |
| Notification body | BGE-M3 dense | Short text |

**Why mix.** Voyage law-2's free 50 M tokens map to roughly 200 MB of cleaned legal text — enough for top-100 cases (Held + Ratio only ≈ 5 MB) and the active statute corpus's operative text. We use BGE-M3 for the long tail (factual passages, notifications) where domain tuning matters less and the open-source model is "free forever".

### 6.2 Hypothetical-Document Embeddings (HyDE) for natural-language queries

Citizen-mode user types *"my landlord is being unreasonable about rent hike"*. Direct embedding loses on lexical sparseness — the relevant text says "section 7 standard rent" not "unreasonable hike".

**HyDE pre-step.** Use gpt-4o-mini (cheap) to draft a one-paragraph hypothetical legal answer. Embed *that* and use it as the retrieval query. This recovers the legal-vocabulary mass that the user's question lacks.

This is opt-in per query — we run HyDE only when the direct embedding has top-3 cosine < 0.4 (i.e., when retrieval signal is weak).

### 6.3 Multi-query expansion

For practitioner mode, run the question through gpt-4o-mini with prompt *"Generate 3 alternative phrasings of this legal question, varying both vocabulary and degree of specificity"*. Embed each and union — ensures different phrasings of the same concept all hit.

### 6.4 Quantisation

Qdrant supports binary (1-bit) and scalar (int8) quantisation. With voyage-law-2 1 024-dim vectors:
- Float32: 4 KB per vector → 4 GB for 1 M vectors → won't fit in 1 GB RAM Qdrant free.
- Int8: 1 KB per vector → 1 GB for 1 M vectors → fits.
- Binary: 128 B per vector → 128 MB for 1 M vectors → trivially fits, with ~5 % recall@10 drop that's recovered by the rerank stage.

**Decision.** Binary quantisation for cold storage with a re-rank rescore on the top 200, OR int8 quantisation. Both let us fit the full active corpus + top-100 cases in the free tier.

---

## 7. Retrieval strategy — the SOTA pipeline

```
User query
  ▼
[Classify + persona-tune retrieval params]
  ▼
[HyDE if support density < 0.4]
  ▼
[Multi-query expansion (practitioner only)]
  ▼
[Three parallel retrievers]
  • Dense (voyage-law-2) → Qdrant top-200
  • Sparse (BGE-M3 sparse) → Qdrant top-200
  • Section-direct (regex parse "Section 138 NI Act" → exact hit) → Qdrant filter
  ▼
[Status filter — drop overruled cases via Neo4j citator query]
  ▼
[Reciprocal Rank Fusion]
  ▼
[Cross-encoder rerank (BGE-reranker-v2)]
  ▼ top 8–20 chunks
[Synthesis (gpt-4o-mini, structured citation output)]
  ▼
[Citation verifier — every cited Section / case must exist in corpus index]
[NLI claim-check (cheap LLM call) — entails / contradicts / not_supported]
  ▼
[Confidence labelling + transparency banner if 0 verified citations]
  ▼ user-facing answer
```

This is the **CRAG (Corrective RAG)** + **Self-RAG** pattern, hybridised. Each pre-synthesis step is independently observable so we can tune empirically.

---

## 8. State-of-the-art features built on top

These are the features that turn a competent RAG implementation into one law firms will actually buy.

| Feature | What it does | Implementation note |
|---|---|---|
| **Citator drill-down** | Click any case → see every case that cites it, with treatment label and a graph view | Cypher query against Neo4j; visualise with Cytoscape.js |
| **Temporal filter** | "What was the law in 2020?" / "Show only post-1-Jul-2024 BNS regime" | `effective_from / effective_to` filters on Qdrant payload |
| **Jurisdiction filter** | "Maharashtra rent control" only returns MH state law + central law | Payload filter `jurisdiction in [india, MH]` |
| **Adversarial draft** | "What would opposing counsel argue?" | Same retrieval, swap synthesis prompt to opposing-counsel persona |
| **What-if amendment** | "If Bill X passes, how does my contract change?" | Pull bill text; diff with current Act; re-run analysis |
| **Document review** | Upload SHA / NDA / employment letter; clause-level risk highlights | Per-clause classifier + retrieval against the clause type |
| **Multilingual (Hindi)** | Type in Hindi; retrieval still finds English statute; answer bilingual | BGE-M3 native multilingual + LLM bilingual output |
| **Multi-turn memory** (the Stanford weak-spot) | Conversational follow-ups recall earlier context | Conversation summary stored on each turn, prepended to next-turn retrieval query |
| **"Why might this answer be wrong?"** | Self-flagged caveats per answer | Synthesis prompt explicitly asks the model to enumerate known limitations of its answer |
| **Confidence-floor refusal** | Refuses when retrieval support is weak; surfaces nearest 3 chunks (already shipped) | `support_density < 0.22` → constructive refusal |
| **Verbatim quote checking** | Quoted passages must appear in the source verbatim | rapidfuzz substring match — already shipped |
| **Cited-pages PDF export** | Generate a court-quality memo with hyperlinked citations | LaTeX template + chunk → PDF |

---

## 9. Top 100 cases — concrete acquisition plan

Source of truth: cross-reference [Wikipedia: Landmark decisions in India](https://en.wikipedia.org/wiki/List_of_landmark_court_decisions_in_India) ∩ [Supreme Court of India landmark summaries](https://www.sci.gov.in/landmark-judgment-summaries/) ∩ [SC Observer top 10 of each year](https://www.scobserver.in) (2018–2025). Where editorially curated lists disagree, prefer SC Observer (legal journalism, transparent methodology).

Provisional list, by area (will be finalised against the three sources above):

**Constitutional law (35).** Kesavananda Bharati v. State of Kerala (1973), Maneka Gandhi v. UoI (1978), Minerva Mills v. UoI (1980), Indra Sawhney v. UoI (1992), SR Bommai v. UoI (1994), Olga Tellis v. BMC (1985, ✅ in corpus), K.S. Puttaswamy v. UoI (2017), Navtej Singh Johar v. UoI (2018), Joseph Shine v. UoI (2018), Shayara Bano v. UoI (2017), Common Cause v. UoI (2018), Vishaka v. Rajasthan (1997), ADM Jabalpur v. Shivkant Shukla (1976), Golaknath v. Punjab (1967), I.R. Coelho v. Tamil Nadu (2007), L. Chandra Kumar v. UoI (1997), Ashok Kumar Thakur v. UoI (2008), M Nagaraj v. UoI (2006), Madhu Limaye v. SDM Monghyr (1971), Sunil Batra v. Delhi Admin (1978), Maru Ram v. UoI (1980), Bandhua Mukti Morcha v. UoI (1984), Hussainara Khatoon v. Bihar (1979), Sheela Barse v. UoI (1986), Bachan Singh v. Punjab (1980), Mithu v. Punjab (1983), Macchi Singh v. Punjab (1983), Shreya Singhal v. UoI (2015), Sabarimala (Indian Young Lawyers Assn. v. Kerala) (2018), Pegasus / Manohar Lal Sharma (2021), Anuradha Bhasin v. UoI (2020), Justice K.S. Puttaswamy v. UoI (Aadhaar — 2018), Mukesh Kumar v. State of Uttarakhand (2020), Coelho I.R., S.G. Vombatkere etc.

**Criminal law (25).** Lalita Kumari v. UoI (2014), Arnesh Kumar v. State of Bihar (2014), DK Basu v. State of WB (1997), Joginder Kumar v. UP (1994), Selvi v. Karnataka (2010), Mohd. Ahmed Khan v. Shah Bano (1985), Sushil Sharma v. State NCT (2014), Hardeep Singh v. Punjab (2014), Ramesh Kumari v. State NCT (2006), CBI v. State of Rajasthan (2001), State of Haryana v. Bhajan Lal (1992), Kamlesh Kumari v. State of UP, BS Joshi v. Haryana (2003), Kapil Mishra cases, Arnab Goswami v. UoI (2020), Vinod Dua v. UoI (2021), Romila Thapar v. UoI (2018), Rambabu Singh Thakur v. Sunil Arora (2020), Mukesh & Anr. v. State (NCT) (2017 — Nirbhaya), Sushil Murmu v. State of Jharkhand (2003), etc.

**Civil / commercial / contract (25).** Vidya Drolia v. Durga Trading (2020) — arbitrability framework, Ssangyong Engineering v. NHAI (2019), Vijay Karia v. Prysmian Cavi (2020), BALCO v. Kaiser Aluminium (2012), ONGC v. Saw Pipes (2003), Renusagar Power v. General Electric (1994), Bharat Aluminium Co. (BALCO) v. Kaiser Aluminium (2016), Salem Advocate Bar Assn. v. UoI, NN Global Mercantile v. Indo Unique Flame (2023), TRF Ltd v. Energo Engineering (2017), Perkins Eastman Architects v. HSCC (2019), Indus Mobile v. Datawind (2017), etc.

**Family / personal law (10).** Vineeta Sharma v. Rakesh Sharma (2020), Sarla Mudgal v. UoI (1995), Lily Thomas v. UoI (2000), Daniel Latifi v. UoI (2001), Indra Sarma v. VKV Sarma (2013), Githa Hariharan v. RBI (1999), Danial Latifi & Anr v. Union Of India, Independent Thought v. UoI (2017), etc.

**Tax / corporate (5).** Vodafone International Holdings v. UoI (2012), CIT v. Vatika Township (2014), Maxopp Investment v. CIT (2018), AAR rulings on key cross-border issues.

This is **finalised** by running the cross-reference at acquisition time against authoritative sources. The list is encoded in `scripts/build_top100_cases.py` so re-runs are deterministic.

---

## 10. Latest amendments — monthly cron

Monthly GitHub Action:

1. Pull `egazette.gov.in` "Notifications" published in the last 30 days for `Ministry of Law and Justice`, `Finance`, `Corporate Affairs`, `Communications`, `MeitY`, `Home Affairs`, `Labour`, `Consumer Affairs`.
2. Diff against existing corpus by `(act_short, section_number)`.
3. New amendments → new chunks (mark `effective_from`); modifications → mark old chunk with `effective_to` and create a new chunk with the post-amendment text.
4. Re-embed only deltas; upsert to Qdrant.
5. Notify maintainer Slack channel with a digest.

This keeps BNS supplementary notifications, DPDP Rules, GST rate revisions, IT Rules amendments, etc. fresh without manual touch.

---

## 11. Implementation plan — staged

### Phase 0 — current state (shipped)
- Citation-faithful by construction ✅
- Hybrid retrieval (dense + lexical + section-direct) ✅
- Status-aware (basic — IPC docs marked `repealed`) ✅
- 81 chunks across 40 docs ✅
- Live on Vercel + Supabase pgvector ✅

### Phase 1 — cloud-native vector DB + reranker (1 week)
1. Provision Qdrant Cloud free cluster.
2. Wire `app/db/qdrant_store.py` (new) alongside existing pgvector store; runtime selector based on `VECTOR_BACKEND` env.
3. Self-host BGE-reranker-v2-m3 on Hugging Face Inference Endpoints free tier OR a single $5/month Hetzner VPS.
4. Add the rerank stage to the agent.
5. Re-run the 15-query audit; expect recall@5 to climb from current numbers.

### Phase 2 — Top 100 cases ingestion (1 week)
1. `scripts/build_top100_cases.py` materialises the canonical list from SC Observer + SC India + Wikipedia; deduplicates; stores citations.
2. Per-case scraper from Indian Kanoon (HTML → structured JSON via per-court parsers).
3. Per-case chunker (Headnote / Held / Ratio / Facts / Obiter).
4. Embed Held + Ratio with voyage-law-2 (paid bucket); Facts with BGE-M3 (free).
5. Citator graph: extract every "Citation A v. Citation B" pattern in body; create Neo4j edges with treatment labels by simple lexical patterns ("approved", "overruled", "distinguished", "doubted").

### Phase 3 — Constitution + active acts full ingestion (1 week)
1. Pull Constitution from `legislative.gov.in` (single PDF, structured).
2. Per-act scraper for the 30-act priority list in `CORPUS.md`.
3. Multi-vector embedding (headline + operative-200 + full).
4. Index into Qdrant with all payload fields populated.

### Phase 4 — SOTA features (2–4 weeks)
1. HyDE for weak-signal queries.
2. Multi-query expansion for practitioner mode.
3. Citator drill-down UI (graph view).
4. Temporal + jurisdiction filters in the UI.
5. Document review (clause-level analysis).

### Phase 5 — production hardening (ongoing)
1. Monthly amendment cron.
2. Eval suite expansion (the existing 6 suites + add temporal-correctness, jurisdiction-correctness, citator-respects-overruled).
3. Cost dashboards (per-query OpenAI cost, Qdrant utilisation, Neo4j utilisation).
4. Per-tenant data residency story for law-firm contracts.

---

## 12. Testing plan — beats Stanford's bar

Stanford's empirical benchmark for legal RAG had 200 queries spanning 9 task types. We replicate and extend:

| Suite | Items | Threshold | Tools |
|---|---|---|---|
| **Citation faithfulness** (existing) | 8 → expand to 100 | 100 % verified | pytest |
| **Adversarial hallucination** (existing) | 8 → expand to 50 | 100 % stripped | pytest |
| **Refusal correctness** (existing) | 8 → expand to 50 | ≥ 90 % | pytest |
| **BNS-currency** (existing) | 5 → expand to 30 | ≥ 90 % | pytest |
| **Persona differentiation** (existing) | 3 → expand to 20 | divergence threshold | pytest |
| **Retrieval recall** (existing) | 13 → expand to 200 | recall@5 ≥ 0.85, recall@10 ≥ 0.95 | pytest |
| **Multi-turn conversation** (NEW — Stanford weakness) | 30 multi-turn dialogues | recall@5 ≥ 0.70 (vs Stanford's 0.33 baseline) | pytest |
| **Multi-jurisdictional reasoning** (NEW) | 25 queries spanning 2+ jurisdictions | accuracy drop < 7 points (vs Stanford's 14) | pytest |
| **Temporal correctness** (NEW) | 20 "what was the law in year X" queries | ≥ 95 % cite the right vintage | pytest |
| **Citator-respects-overruled** (NEW) | 15 queries about overruled cases | 100 % must mention overruling status | pytest |
| **Quote-fidelity** (NEW) | 30 queries asking for verbatim quotes | quote substring match 100 % | pytest |

Total: ~ 500 evals. Run on every deploy; fail the deploy if any threshold is breached.

The two **NEW** suites that target Stanford-identified weak points (multi-turn, multi-jurisdiction) are the headline differentiator — this is where we publish numbers and beat the published bar.

---

## 13. Trade-offs and known limitations (honest)

| Choice | Cost | Trade-off |
|---|---|---|
| Voyage law-2 | $0 free quota, then $0.05/M | Vendor lock-in for the legal-tuned variant; mitigation = abstract via embedding interface so we can swap to BGE-M3-fine-tuned later |
| Qdrant Cloud free | $0 | 1 GB RAM cap; binary quantisation buys headroom but with ~5% recall@10 hit; rescore stage compensates |
| Neo4j AuraDB free | $0 | 50K node cap; if we exceed (i.e., scale to all SC + 5 HCs ≈ millions of judgments), need self-host or paid tier |
| Self-hosted BGE-reranker | $5/month VPS | Operationally we run a small VM; or use HF Inference Endpoints free hours |
| HyDE adds an LLM call | ~$0.0001 / query | Only fires when retrieval is weak; net cost negligible |
| Multi-query expansion | 1 LLM call / query | Only practitioner mode; ~$0.0002 /query |
| Cross-encoder rerank | 200 ms / query | Worth it; removes the long tail of irrelevant retrieval |

**The bar we cannot beat without paid resources.**
- 50K judgments + amendments + circulars + state acts + treatises = ~50–100M chunks. That requires either a paid Qdrant tier (€100/month) or self-hosted Qdrant (€10/month VPS) with 10× more storage. Free tier is sufficient for the demo + top-100 cases + active statutes scope; not for "every judgment ever".

---

## 14. What we ship in 4 weeks (concrete)

- Live demo at the existing URL with **the top 100 SC cases + Constitution + 30 active central acts** fully ingested into Qdrant Cloud.
- Citator graph in Neo4j AuraDB with edges for every citation in those 100 cases.
- Reranker stage (BGE-reranker-v2) live in the agent.
- HyDE for weak-signal queries.
- Multi-turn conversation memory (the Stanford weakness).
- 500-item eval suite with published numbers vs the Stanford baseline.
- Monthly cron for amendments.

This is the 4-week deliverable that turns the demo into a credible product for Indian law firms and a reference architecture for international ones.

---

## Sources

- [Qdrant pricing](https://qdrant.tech/pricing/) — free tier 1 GB RAM / 4 GB disk forever
- [Pinecone Starter free tier](https://community.pinecone.io/t/limit-of-vectors-on-free-plan/3821) — 100 K vectors, paused after 3 weeks inactivity
- [Voyage AI pricing](https://docs.voyageai.com/docs/pricing) — voyage-law-2 50 M tokens free
- [Neo4j AuraDB free](https://neo4j.com/product/auradb/) — 50 K nodes / 175 K relationships
- [Cohere rate limits](https://docs.cohere.com/docs/rate-limits) — Trial 1 000 calls/month
- [BAAI/bge-m3 model card](https://huggingface.co/BAAI/bge-m3) — hybrid retrieval in one model
- [Stanford HAI: AI on Trial — Legal Models Hallucinate](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries) — 17–33% hallucination in Lexis+ AI / Practical Law AI
- [Stanford Legal RAG Hallucinations paper](https://law.stanford.edu/wp-content/uploads/2024/05/Legal_RAG_Hallucinations.pdf) — methodology and findings
- [Wikipedia: Landmark court decisions in India](https://en.wikipedia.org/wiki/List_of_landmark_court_decisions_in_India)
- [Supreme Court of India landmark summaries](https://www.sci.gov.in/landmark-judgment-summaries/)
- [SC Observer annual reviews](https://www.scobserver.in)
- [LLRX legal-RAG hallucinations summary](https://www.llrx.com/2026/02/what-the-science-says-about-hallucinations-in-legal-research/)
