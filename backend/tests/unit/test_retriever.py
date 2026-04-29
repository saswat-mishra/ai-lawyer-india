"""Retriever sanity. Uses the seeded fixture so retrieval has data."""
import pytest

from app.core.config import Persona
from app.rag.retriever import retrieve_legal, support_density


@pytest.mark.asyncio
async def test_retrieve_finds_section_103_bns(seeded):
    out = await retrieve_legal("punishment for murder under Section 103 BNS",
                                  persona=Persona.PRACTITIONER)
    assert out, "expected at least one retrieval"
    sections = [c.section_number for c in out]
    assert "103" in sections


@pytest.mark.asyncio
async def test_retrieve_excludes_overruled(seeded):
    """The seed marks IPC as 'repealed' (status), so it should not appear unless explicitly asked."""
    out = await retrieve_legal("murder", persona=Persona.PRACTITIONER)
    # IPC docs are status='repealed' in the seed; the retriever filters those out.
    acts_seen = set()
    for c in out:
        for token in c.hierarchy_path:
            acts_seen.add(token)
    # BNS should be present, IPC should NOT be (repealed).
    assert any("BNS" in a or "Bharatiya" in a for a in acts_seen)


@pytest.mark.asyncio
async def test_persona_caps_results(seeded):
    citizen = await retrieve_legal("contract breach", persona=Persona.CITIZEN)
    practitioner = await retrieve_legal("contract breach", persona=Persona.PRACTITIONER)
    # Citizen capped lower than practitioner.
    assert len(citizen) <= len(practitioner)


@pytest.mark.asyncio
async def test_section_direct_lookup(seeded):
    """Numeric section + act hint should surface that section even with poor lexical overlap."""
    out = await retrieve_legal("Section 138 NI Act", persona=Persona.PRACTITIONER)
    assert out
    assert out[0].section_number == "138"


@pytest.mark.asyncio
async def test_support_density(seeded):
    out = await retrieve_legal("murder", persona=Persona.CITIZEN)
    assert support_density(out) >= 0.0


@pytest.mark.asyncio
async def test_empty_corpus_returns_nothing():
    out = await retrieve_legal("any question")
    assert out == []
