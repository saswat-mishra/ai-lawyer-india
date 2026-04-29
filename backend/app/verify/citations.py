"""Citation parser + verifier.

Citations are emitted by the synthesis step as structured JSON, but we also
parse free-text citations for robustness. The verifier checks each against
the corpus index; unverified citations are stripped from the user-facing
output and replaced with a "[unverified]" tag in the audit trail.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from rapidfuzz import fuzz

from app.db import store


# ---------- Models ----------


@dataclass
class Citation:
    type: str                         # "section" | "case" | "constitution"
    raw: str                          # original text as emitted
    act: str | None = None
    section: str | None = None
    case_name: str | None = None
    citation_str: str | None = None   # e.g. 'AIR 1986 SC 180'
    paragraph: int | None = None
    quoted_text: str | None = None    # if a quote accompanies the citation
    chunk_id: str | None = None       # set after verification

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "raw": self.raw,
            "act": self.act,
            "section": self.section,
            "case_name": self.case_name,
            "citation_str": self.citation_str,
            "paragraph": self.paragraph,
            "quoted_text": self.quoted_text,
            "chunk_id": self.chunk_id,
        }


@dataclass
class VerificationResult:
    verified: list[Citation] = field(default_factory=list)
    unverified: list[Citation] = field(default_factory=list)
    quote_failures: list[Citation] = field(default_factory=list)

    @property
    def faithful(self) -> bool:
        return not (self.unverified or self.quote_failures)


# ---------- Parsing ----------


_SECTION_PAT = re.compile(
    r"""
    (?:Section|S\.|Sec\.?|§)\s*
    (?P<sec>\d+[A-Z]*(?:\([^)]+\))?)
    \s*(?:of\s+the\s+)?
    (?P<act>
        # 1. Bare short form: BNS, IPC, NI Act, CrPC, BNSS, BSA, CPC
        (?:BNS|BNSS|BSA|IPC|CrPC|CPC|NI\s+Act)
        |
        # 2. Long form ending in keyword (e.g., "Indian Penal Code", "Made-Up Act")
        [A-Z][A-Za-z &.,'\-]{0,80}?(?:Act|Code|Sanhita|Adhiniyam)
    )
    """,
    re.X,
)

# "Article 21 of the Constitution", "Article 14 of the Indian Constitution"
_ARTICLE_PAT = re.compile(
    r"Article\s+(?P<sec>\d+[A-Z]*(?:\([^)]+\))?)"
    r"(?:\s+of\s+the\s+(?:Indian\s+)?Constitution)?",
    re.I,
)

# Short-form citations e.g. 'AIR 1986 SC 180', '(2017) 4 SCC 312', '2023 SCC OnLine SC 99'
_CASE_CITE_PAT = re.compile(
    r"""
    (?:
        AIR\s+\d{4}\s+(?:SC|All|Bom|Cal|Mad|Del|Kar|Ker|Pat|Raj|MP|Ori|Punj|Hyd|Guj|HP|J&K|Sikk|Megh|Tri|Manip|Mizo|Nag|Aru|Chhat|Jhar|Utt|And)\s+\d+
        |
        \(\d{4}\)\s+\d+\s+SCC\s+\d+
        |
        \d{4}\s+SCC\s*OnLine\s+(?:SC|HC[A-Za-z\-]*|[A-Z][A-Za-z]+)\s+\d+
    )
    """,
    re.X,
)

_CASE_NAME_PAT = re.compile(
    r"([A-Z][A-Za-z.&'\- ]{1,60}?)\s+v(?:s|s?\.)?\s+([A-Z][A-Za-z.&'\- ]{1,80})",
)


# Bracket-tag form the synthesis prompt asks the model to emit, plus tolerant
# variants the model sometimes drifts into (e.g., [BNS:Chapter VI:103]).
_BRACKET_TAG_PAT = re.compile(
    r"\[(?:SECT:)?(?P<act>BNS|BNSS|BSA|IPC|CrPC|CPC|NI\s*Act|Constitution|Contract\s*Act|TP\s*Act|CPA(?:\s*\d{4})?|Companies(?:\s*Act)?|DPDP(?:\s*Act)?)"
    r"[^\]]*?"
    r"(?P<sec>\d+[A-Z]*(?:\([^)]+\))?)"
    r"[^\]]*\]",
    re.I,
)
_CASE_TAG_PAT = re.compile(r"\[CASE:(?P<cite>[^\]]+)\]")


def parse_citations(text: str) -> list[Citation]:
    """Parse all section / case citations in `text`. Conservative — false negatives
    are OK, false positives are not (the verifier will catch them but it's cleaner
    to start narrow).
    """
    out: list[Citation] = []
    seen: set[tuple[str, str | None]] = set()

    # 1. Prose sections: "Section 103 BNS"
    for m in _SECTION_PAT.finditer(text):
        act = _normalise_act(m.group("act"))
        sec = m.group("sec")
        if (act, sec) in seen:
            continue
        seen.add((act, sec))
        out.append(Citation(type="section", raw=m.group(0), act=act, section=sec))

    # 2. Bracket tags: "[SECT:BNS:103]" or "[BNS:Chapter VI:103]" model-drift form.
    for m in _BRACKET_TAG_PAT.finditer(text):
        act = _normalise_act(m.group("act"))
        sec = m.group("sec")
        if (act, sec) in seen:
            continue
        seen.add((act, sec))
        out.append(Citation(type="section", raw=m.group(0), act=act, section=sec))

    # 3. Articles of the Constitution.
    for m in _ARTICLE_PAT.finditer(text):
        sec = m.group("sec")
        key = ("Constitution", sec)
        if key in seen:
            continue
        seen.add(key)
        out.append(Citation(type="section", raw=m.group(0),
                              act="Constitution", section=sec))

    # 3. Case citations.
    for m in _CASE_CITE_PAT.finditer(text):
        head = text[max(0, m.start() - 200):m.start()]
        name_match = _CASE_NAME_PAT.search(head)
        out.append(Citation(
            type="case", raw=m.group(0),
            case_name=(f"{name_match.group(1).strip()} v. {name_match.group(2).strip()}"
                        if name_match else None),
            citation_str=m.group(0),
        ))
    for m in _CASE_TAG_PAT.finditer(text):
        out.append(Citation(type="case", raw=m.group(0), citation_str=m.group("cite")))

    return out


def _normalise_act(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip().rstrip(",.;")
    # Long-form -> canonical short form.
    aliases = {
        "Bharatiya Nyaya Sanhita": "BNS",
        "Bharatiya Nagarik Suraksha Sanhita": "BNSS",
        "Bharatiya Sakshya Adhiniyam": "BSA",
        "Indian Penal Code": "IPC",
        "Code of Criminal Procedure": "CrPC",
        "Negotiable Instruments Act": "NI Act",
        "Code of Civil Procedure": "CPC",
        "Indian Contract Act": "Contract Act",
        "Transfer of Property Act": "TP Act",
        "Consumer Protection Act, 2019": "CPA 2019",
        "Consumer Protection Act 2019": "CPA 2019",
        "Consumer Protection Act": "CPA 2019",
        "Constitution of India": "Constitution",
    }
    for full, short in aliases.items():
        if full.lower() in s.lower():
            return short
    # Short bare forms (already-normalised).
    upper = s.upper().replace(" ACT", " Act")
    for canon in ("BNS", "BNSS", "BSA", "IPC", "CrPC", "CPC"):
        if upper == canon.upper() or upper.startswith(canon.upper() + " "):
            return canon
    if upper.startswith("NI ACT") or upper == "NI ACT":
        return "NI Act"
    if upper == "CONSTITUTION" or upper.startswith("CONSTITUTION "):
        return "Constitution"
    if upper == "TP ACT":
        return "TP Act"
    return s


# ---------- Verification ----------


async def verify_citations(citations: list[Citation], *,
                            evidence_chunks: list[dict[str, Any]] | None = None
                            ) -> VerificationResult:
    """Check each citation against the corpus.

    Section citations: lookup `find_section_by_number(act, section)` in the store.
    Case citations: case-insensitive substring match of citation_str against any
        legal_document.short_citation or long_citation.
    Quote check: if `quoted_text` is set, must appear (fuzz >=85) in any retrieved
        evidence chunk.
    """
    result = VerificationResult()
    docs = await store.list_legal_documents()
    chunks = await store.list_legal_chunks()

    for cit in citations:
        ok = False
        if cit.type == "section" and cit.act and cit.section:
            chunk = await store.find_section_by_number(cit.act, cit.section)
            if chunk:
                cit.chunk_id = chunk["id"]
                ok = True
        elif cit.type == "case" and cit.citation_str:
            target = cit.citation_str.lower()
            for d in docs:
                short = (d.get("short_citation") or "").lower()
                long = (d.get("long_citation") or "").lower()
                if target in short or target in long:
                    cit.chunk_id = d["id"]
                    ok = True
                    break

        if not ok:
            result.unverified.append(cit)
            continue

        # Quote check.
        if cit.quoted_text:
            quote = cit.quoted_text.strip()
            haystacks = []
            if evidence_chunks:
                haystacks.extend(c.get("text", "") for c in evidence_chunks)
            if cit.chunk_id:
                full = next((c for c in chunks if c["id"] == cit.chunk_id), None)
                if full:
                    haystacks.append(full["text"])
            if not any(_quote_present(quote, h) for h in haystacks):
                result.quote_failures.append(cit)
                continue

        result.verified.append(cit)

    return result


def _quote_present(quote: str, haystack: str, threshold: int = 85) -> bool:
    if not quote or not haystack:
        return False
    if quote.lower() in haystack.lower():
        return True
    return fuzz.partial_ratio(quote.lower(), haystack.lower()) >= threshold


def strip_unverified(text: str, result: VerificationResult) -> str:
    """Replace any unverified citation's raw text in `text` with [unverified]."""
    flagged = [*result.unverified, *result.quote_failures]
    out = text
    for c in flagged:
        out = out.replace(c.raw, "[unverified citation removed]")
    return out
