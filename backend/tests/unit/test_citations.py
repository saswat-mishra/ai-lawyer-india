"""Citation parsing + verification."""
import pytest

from app.verify.citations import (Citation, parse_citations, strip_unverified,
                                      verify_citations)


def test_parse_section():
    text = "Per Section 103 BNS, murder is..."
    out = parse_citations(text)
    assert any(c.type == "section" and c.section == "103" and c.act == "BNS" for c in out)


def test_parse_legacy_act():
    text = "Section 138 of the Negotiable Instruments Act applies."
    out = parse_citations(text)
    assert any(c.type == "section" and c.section == "138" and c.act in {"NI Act"} for c in out)


def test_parse_case_air():
    text = "See AIR 1986 SC 180."
    out = parse_citations(text)
    assert any(c.type == "case" and c.citation_str == "AIR 1986 SC 180" for c in out)


def test_parse_scc():
    text = "(2017) 4 SCC 312"
    out = parse_citations(text)
    assert any(c.type == "case" for c in out)


@pytest.mark.asyncio
async def test_verify_real_section_passes(seeded):
    cit = Citation(type="section", raw="Section 103 BNS", act="BNS", section="103")
    res = await verify_citations([cit])
    assert len(res.verified) == 1
    assert res.faithful


@pytest.mark.asyncio
async def test_verify_fake_section_flagged(seeded):
    cit = Citation(type="section", raw="Section 9999 BNS", act="BNS", section="9999")
    res = await verify_citations([cit])
    assert len(res.unverified) == 1
    assert not res.faithful


@pytest.mark.asyncio
async def test_strip_unverified_replaces_text(seeded):
    cit = Citation(type="section", raw="Section 9999 BNS", act="BNS", section="9999")
    res = await verify_citations([cit])
    out = strip_unverified("As per Section 9999 BNS, this is bogus.", res)
    assert "9999" not in out
    assert "[unverified" in out


@pytest.mark.asyncio
async def test_quote_check(seeded):
    cit = Citation(type="section", raw="Section 103 BNS", act="BNS", section="103",
                     quoted_text="Whoever commits murder shall be punished with death")
    res = await verify_citations([cit])
    assert res.faithful


@pytest.mark.asyncio
async def test_quote_mismatch_flagged(seeded):
    cit = Citation(type="section", raw="Section 103 BNS", act="BNS", section="103",
                     quoted_text="something completely fabricated that's not in the section")
    res = await verify_citations([cit])
    assert len(res.quote_failures) == 1
