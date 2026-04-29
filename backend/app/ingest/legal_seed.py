"""Seed the legal corpus with a small, hand-curated set of high-value chunks.

Intent: in tests and in early dev, the system has *something* to retrieve so
the agent doesn't always refuse. The full corpus comes from `scripts/`
scrapers; this module is the minimum that makes the test suite meaningful.
"""
from __future__ import annotations

from datetime import date
from typing import Any

from app.db import store
from app.llm.openai_client import embed


SEED_DOCS: list[dict[str, Any]] = [
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Nyaya Sanhita, 2023",
            "short_citation": "BNS", "long_citation": "Bharatiya Nyaya Sanhita, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2024",
        },
        "chunks": [
            {"hierarchy_path": ["BNS", "Chapter VI", "Section 103"],
             "chunk_type": "section", "section_number": "103",
             "text": "Section 103. Punishment for murder.—(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. (2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter X", "Section 318"],
             "chunk_type": "section", "section_number": "318",
             "text": "Section 318. Cheating.—(1) Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person or to consent that any person shall retain any property... is said to 'cheat'. (4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security... shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XIX", "Section 356"],
             "chunk_type": "section", "section_number": "356",
             "text": "Section 356. Defamation.—(1) Whoever, by words either spoken or intended to be read, or by signs or by visible representations, makes or publishes any imputation concerning any person intending to harm... the reputation of such person, is said... to defame that person. (2) Whoever defames another shall be punished with simple imprisonment for a term which may extend to two years, or with fine, or with community service.",
             "metadata": {"act_short": "BNS"}},
        ],
    },
    {
        "doc": {
            "source_type": "central_statute", "title": "Indian Penal Code, 1860",
            "short_citation": "IPC", "long_citation": "Indian Penal Code, 1860",
            "effective_to": "2024-06-30",
            "status": "repealed",  # for offences after 1 Jul 2024
            "source_url": "https://indiacode.nic.in/handle/123456789/2263",
        },
        "chunks": [
            {"hierarchy_path": ["IPC", "Chapter XVI", "Section 302"],
             "chunk_type": "section", "section_number": "302",
             "text": "Section 302. Punishment for murder.—Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
             "metadata": {"act_short": "IPC", "successor": "BNS §103"}},
            {"hierarchy_path": ["IPC", "Chapter XVII", "Section 420"],
             "chunk_type": "section", "section_number": "420",
             "text": "Section 420. Cheating and dishonestly inducing delivery of property.—Whoever cheats and thereby dishonestly induces the person deceived to deliver any property... shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
             "metadata": {"act_short": "IPC", "successor": "BNS §318(4)"}},
        ],
    },
    {
        "doc": {
            "source_type": "central_statute", "title": "Negotiable Instruments Act, 1881",
            "short_citation": "NI Act",
            "long_citation": "Negotiable Instruments Act, 1881",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2189",
        },
        "chunks": [
            {"hierarchy_path": ["NI Act", "Chapter XVII", "Section 138"],
             "chunk_type": "section", "section_number": "138",
             "text": "Section 138. Dishonour of cheque for insufficiency, etc., of funds in the account.—Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid... such person shall be deemed to have committed an offence and shall, without prejudice to any other provision of this Act, be punished with imprisonment for a term which may extend to two years, or with fine which may extend to twice the amount of the cheque, or with both.",
             "metadata": {"act_short": "NI Act"}},
        ],
    },
    {
        "doc": {
            "source_type": "central_statute", "title": "Indian Contract Act, 1872",
            "short_citation": "Contract Act",
            "long_citation": "Indian Contract Act, 1872",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2187",
        },
        "chunks": [
            {"hierarchy_path": ["Contract Act", "Chapter VI", "Section 73"],
             "chunk_type": "section", "section_number": "73",
             "text": "Section 73. Compensation for loss or damage caused by breach of contract.—When a contract has been broken, the party who suffers by such breach is entitled to receive, from the party who has broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose in the usual course of things from such breach, or which the parties knew, when they made the contract, to be likely to result from the breach of it.",
             "metadata": {"act_short": "Contract Act"}},
            {"hierarchy_path": ["Contract Act", "Chapter II", "Section 27"],
             "chunk_type": "section", "section_number": "27",
             "text": "Section 27. Agreement in restraint of trade, void.—Every agreement by which any one is restrained from exercising a lawful profession, trade or business of any kind, is to that extent void.",
             "metadata": {"act_short": "Contract Act"}},
        ],
    },
    {
        "doc": {
            "source_type": "central_statute", "title": "Transfer of Property Act, 1882",
            "short_citation": "TP Act",
            "long_citation": "Transfer of Property Act, 1882",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["TP Act", "Chapter V", "Section 106"],
             "chunk_type": "section", "section_number": "106",
             "text": "Section 106. Duration of certain leases in absence of written contract or local usage.—In the absence of a contract or local law or usage to the contrary, a lease of immovable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, by six months' notice; and a lease of immovable property for any other purpose shall be deemed to be a lease from month to month, terminable, on the part of either lessor or lessee, by fifteen days' notice.",
             "metadata": {"act_short": "TP Act"}},
        ],
    },
    {
        "doc": {
            "source_type": "central_statute", "title": "Consumer Protection Act, 2019",
            "short_citation": "CPA 2019",
            "long_citation": "Consumer Protection Act, 2019",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CPA 2019", "Chapter II", "Section 2(11)"],
             "chunk_type": "section", "section_number": "2(11)",
             "text": "Deficiency means any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance which is required to be maintained by or under any law for the time being in force or has been undertaken to be performed by a person in pursuance of a contract or otherwise in relation to any service.",
             "metadata": {"act_short": "CPA 2019"}},
        ],
    },
    {
        "doc": {
            "source_type": "case", "title": "Olga Tellis v. Bombay Municipal Corporation",
            "short_citation": "AIR 1986 SC 180",
            "long_citation": "Olga Tellis v. Bombay Municipal Corporation, AIR 1986 SC 180; (1985) 3 SCC 545",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Olga Tellis v. BMC", "AIR 1986 SC 180", "Held"],
             "chunk_type": "held", "section_number": None,
             "text": "The right to life under Article 21 of the Constitution includes the right to livelihood. Eviction of pavement dwellers without due process violates this right. Procedural due process under Article 21 requires reasonable opportunity to be heard before eviction.",
             "metadata": {"citation": "AIR 1986 SC 180"}},
        ],
    },
    {
        "doc": {
            "source_type": "constitution", "title": "Constitution of India",
            "short_citation": "Constitution",
            "long_citation": "Constitution of India",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Constitution", "Part III", "Article 21"],
             "chunk_type": "article", "section_number": "21",
             "text": "Article 21. Protection of life and personal liberty.—No person shall be deprived of his life or personal liberty except according to procedure established by law.",
             "metadata": {}},
            {"hierarchy_path": ["Constitution", "Part III", "Article 14"],
             "chunk_type": "article", "section_number": "14",
             "text": "Article 14. Equality before law.—The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
             "metadata": {}},
        ],
    },
]


SEED_MAPPINGS: list[tuple[str, str, str, str, str]] = [
    ("IPC", "302", "BNS", "103", "Punishment for murder"),
    ("IPC", "420", "BNS", "318(4)", "Cheating and dishonestly inducing delivery"),
    ("IPC", "499", "BNS", "356(1)", "Defamation (definition)"),
    ("IPC", "500", "BNS", "356(2)", "Punishment for defamation"),
    ("CrPC", "154", "BNSS", "173", "First Information Report"),
    ("Indian Evidence Act", "65B", "BSA", "63", "Admissibility of electronic records"),
]


async def seed_legal_corpus() -> dict[str, int]:
    """Idempotent seed loader.

    Preference order:
    1. `backend/data/corpus.jsonl` (pre-embedded bundle, fast, no API cost) —
       built offline by `scripts/build_corpus.py`.
    2. Live embedding of SEED_DOCS + EXTRA_SEED_DOCS + TIER1_SEED_DOCS (slow,
       costs OpenAI API; only used when the bundle is missing — useful in
       local dev or first run).
    """
    from app.ingest.embedded_corpus import load_pre_embedded_corpus
    from app.ingest.legal_seed_extra import EXTRA_SEED_DOCS

    existing = await store.list_legal_documents()
    if existing:
        return {"docs": len(existing), "skipped": True}

    # Path 1: pre-embedded bundle.
    pre = await load_pre_embedded_corpus()
    if pre.get("loaded"):
        return pre

    # Path 2: live-embed fallback. Dedupe by (short_citation + title) so the
    # SEED_DOCS / EXTRA / TIER1 splits don't create duplicate doc rows.
    try:
        from app.ingest.legal_seed_tier1 import TIER1_SEED_DOCS
    except Exception:
        TIER1_SEED_DOCS = []
    try:
        from app.ingest.legal_seed_phase1 import PHASE1_SEED_DOCS
    except Exception:
        PHASE1_SEED_DOCS = []
    try:
        from app.ingest.legal_seed_constitution import CONSTITUTION_SEED
        CONSTITUTION_DOCS = [CONSTITUTION_SEED]
    except Exception:
        CONSTITUTION_DOCS = []
    try:
        from app.ingest.legal_seed_cases import CASE_SEED_DOCS
    except Exception:
        CASE_SEED_DOCS = []
    try:
        from app.ingest.legal_seed_phase2 import PHASE2_SEED_DOCS
    except Exception:
        PHASE2_SEED_DOCS = []

    deduped: dict[tuple[str, str], dict] = {}
    for entry in (
        SEED_DOCS + EXTRA_SEED_DOCS + TIER1_SEED_DOCS
        + PHASE1_SEED_DOCS + CONSTITUTION_DOCS
        + CASE_SEED_DOCS + PHASE2_SEED_DOCS
    ):
        key = (entry["doc"].get("short_citation") or "", entry["doc"].get("title") or "")
        if key in deduped:
            deduped[key]["chunks"].extend(entry["chunks"])
        else:
            deduped[key] = {"doc": dict(entry["doc"]), "chunks": list(entry["chunks"])}

    counts = {"docs": 0, "chunks": 0}
    for entry in deduped.values():
        doc = await store.insert_legal_document(**entry["doc"])
        chunk_texts = [c["text"] for c in entry["chunks"]]
        embeddings = await embed(chunk_texts)
        for chunk, vec in zip(entry["chunks"], embeddings):
            await store.insert_legal_chunk(
                document_id=doc["id"],
                hierarchy_path=chunk["hierarchy_path"],
                chunk_type=chunk["chunk_type"],
                section_number=chunk.get("section_number"),
                text=chunk["text"],
                embedding=vec,
                metadata=chunk.get("metadata", {}),
            )
            counts["chunks"] += 1
        counts["docs"] += 1

    for old_act, old_sec, new_act, new_sec, notes in SEED_MAPPINGS:
        await store.add_statute_mapping(old_act, old_sec, new_act, new_sec, notes)

    # Seed citator graph (best-effort).
    try:
        from app.rag.citator import seed_citator_graph
        counts["citator"] = await seed_citator_graph()
    except Exception:
        pass

    return counts
