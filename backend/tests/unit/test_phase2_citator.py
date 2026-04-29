"""Phase 2.3 — citator extraction + graph seeding."""
import pytest

from app.rag.citator import (
    extract_citations_from_text,
    KNOWN_TREATMENTS,
    normalise_citation,
)


def test_extract_scc_citation():
    txt = "The Court followed (1973) 4 SCC 225 in basic structure analysis."
    found = extract_citations_from_text(txt)
    assert any("(1973) 4 SCC 225" in f["citation"] for f in found)


def test_extract_air_citation():
    txt = "Per AIR 1986 SC 180, the right under Article 21 is not absolute."
    found = extract_citations_from_text(txt)
    assert any("AIR 1986 SC 180" in f["citation"] for f in found)


def test_extract_overruled_treatment():
    txt = "The earlier holding in (1976) 2 SCC 521 was expressly overruled."
    found = extract_citations_from_text(txt)
    assert found and found[0]["treatment"] == "overruled"


def test_extract_distinguished_treatment():
    txt = "On the facts, the Court distinguished AIR 1962 SC 1296 and proceeded."
    found = extract_citations_from_text(txt)
    assert found and found[0]["treatment"] == "distinguished"


def test_extract_followed_default_when_no_keyword():
    txt = "See (2017) 10 SCC 1 for the privacy framework."
    found = extract_citations_from_text(txt)
    assert found and found[0]["treatment"] == "referred"


def test_known_treatments_contain_keystone_pairs():
    """Sanity: the curated table should include the most-cited pairs."""
    pairs = {(s, d) for s, d, _, _ in KNOWN_TREATMENTS}
    # Minerva Mills follows Kesavananda
    assert ("(1980) 3 SCC 625", "(1973) 4 SCC 225") in pairs
    # Puttaswamy overrules ADM Jabalpur
    assert ("(2017) 10 SCC 1", "AIR 1976 SC 1207") in pairs


def test_citation_normalisation_collapses_whitespace():
    assert normalise_citation("AIR  1986  SC  180") == "AIR 1986 SC 180"
    assert normalise_citation("  (1973)  4  SCC  225 ") == "(1973) 4 SCC 225"


@pytest.mark.asyncio
async def test_citator_seeding_idempotent(monkeypatch):
    """When the same case_citation is added twice, the second is rejected."""
    from app.db import store
    # Reset memory store to be hermetic.
    store._mem.case_citations.clear()

    a = await store.insert_legal_document(
        source_type="case", title="Case A",
        short_citation="A1", long_citation="A1", status="in_force",
    )
    b = await store.insert_legal_document(
        source_type="case", title="Case B",
        short_citation="B1", long_citation="B1", status="in_force",
    )
    ok1 = await store.add_case_citation(
        source_doc_id=a["id"], cited_doc_id=b["id"],
        treatment="followed", paragraph=None,
    )
    ok2 = await store.add_case_citation(
        source_doc_id=a["id"], cited_doc_id=b["id"],
        treatment="followed", paragraph=None,
    )
    assert ok1 is True
    assert ok2 is False  # idempotent — duplicate rejected

    rows = await store.list_citations_to(cited_doc_id=b["id"])
    assert len(rows) == 1
    assert rows[0]["treatment"] == "followed"
    assert rows[0]["source_short_citation"] == "A1"
