"""Structurally-aware chunker.

A naive 512-token splitter destroys legal text — it bisects Sections, orphans
provisos, and breaks the unit of legal meaning. This chunker chunks on
*structural* boundaries first, then enforces a soft token cap.

It supports two doc kinds:
- Statutes (Act -> Chapter -> Section -> Subsection -> Proviso -> Explanation)
- Cases (Headnote -> Facts -> Issues -> Held -> Ratio -> Obiter)

Input is plain text with marker conventions (or a parsed dict from the scraper).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Iterator

# Section header patterns commonly used in Indian bare-act renderings.
_SECTION_RE = re.compile(
    r"""
    ^\s*
    (?:Section|S\.|Sec\.|§)\s*    # 'Section', 'S.', 'Sec.', '§'
    (?P<num>\d+[A-Z]*(?:\([^)]+\))?)  # number with optional letter / subnumber
    \s*[\.\:\-]?\s*
    (?P<title>[^\n]*)
    """,
    re.I | re.X,
)

_ARTICLE_RE = re.compile(r"^\s*Article\s+(?P<num>\d+[A-Z]*)\s*[\.\:\-]?\s*(?P<title>[^\n]*)", re.I)
_CHAPTER_RE = re.compile(r"^\s*Chapter\s+(?P<num>[IVXLCDM\d]+)\s*[\.\:\-]?\s*(?P<title>[^\n]*)", re.I)
_PROVISO_RE = re.compile(r"^\s*Provided\s+that\b", re.I)
_EXPLANATION_RE = re.compile(r"^\s*Explanation\b", re.I)

# Case section anchors.
_CASE_HEADERS = {
    "headnote": re.compile(r"^\s*HEADNOTE\b", re.I),
    "facts": re.compile(r"^\s*FACTS\b", re.I),
    "issues": re.compile(r"^\s*(?:ISSUES?|QUESTIONS?\s+FOR\s+CONSIDERATION)\b", re.I),
    "held": re.compile(r"^\s*HELD\b", re.I),
    "ratio": re.compile(r"^\s*RATIO\b", re.I),
    "obiter": re.compile(r"^\s*OBITER\b", re.I),
}


@dataclass
class Chunk:
    text: str
    chunk_type: str
    hierarchy_path: list[str] = field(default_factory=list)
    section_number: str | None = None
    metadata: dict = field(default_factory=dict)

    def token_count(self) -> int:
        # Cheap approximation: 1 token ~= 4 chars. Replace with tiktoken later.
        return max(1, len(self.text) // 4)


def chunk_statute(text: str, *, act_short: str, act_title: str,
                   max_tokens: int = 1000) -> list[Chunk]:
    """Chunk a statute by Section. Subsections roll up into the parent Section
    chunk unless that exceeds max_tokens, in which case we split on subsection
    boundaries (never mid-sentence).
    """
    chunks: list[Chunk] = []
    current_chapter = ""
    buf: list[str] = []
    cur_section: str | None = None
    cur_section_title: str = ""

    def flush():
        if not buf or cur_section is None:
            return
        body = "\n".join(buf).strip()
        if not body:
            return
        path = [act_title]
        if current_chapter:
            path.append(current_chapter)
        path.append(f"Section {cur_section}")
        # Cap by tokens; if too big, split on paragraph boundaries.
        for piece in _split_by_tokens(body, max_tokens):
            chunks.append(Chunk(
                text=piece,
                chunk_type="section",
                hierarchy_path=list(path),
                section_number=cur_section,
                metadata={"act_short": act_short, "section_title": cur_section_title},
            ))

    for line in text.splitlines():
        ch = _CHAPTER_RE.match(line)
        if ch:
            flush()
            buf, cur_section, cur_section_title = [], None, ""
            current_chapter = f"Chapter {ch['num']} {ch['title']}".strip()
            continue
        sec = _SECTION_RE.match(line)
        if sec and not _looks_like_subsection(sec["num"]):
            flush()
            cur_section = sec["num"].strip()
            cur_section_title = (sec["title"] or "").strip()
            buf = [line.strip()]
            continue
        if cur_section is not None:
            buf.append(line.rstrip())

    flush()
    return chunks


def chunk_case(text: str, *, citation: str, case_name: str,
                max_tokens: int = 1200) -> list[Chunk]:
    """Chunk a case judgment by structural anchors.

    If the text doesn't have anchors, fall back to a single 'opinion' chunk.
    """
    chunks: list[Chunk] = []
    sections: list[tuple[str, list[str]]] = []
    current_label = "opinion"
    current_buf: list[str] = []

    def _match_header(line: str) -> str | None:
        for lbl, pat in _CASE_HEADERS.items():
            if pat.match(line):
                return lbl
        return None

    for line in text.splitlines():
        new_label = _match_header(line)
        if new_label is not None:
            if current_buf:
                sections.append((current_label, current_buf))
            current_label = new_label
            current_buf = []
        else:
            current_buf.append(line)

    if current_buf:
        sections.append((current_label, current_buf))

    if not sections:
        sections = [("opinion", text.splitlines())]

    for label, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        for piece in _split_by_tokens(body, max_tokens):
            chunks.append(Chunk(
                text=piece,
                chunk_type=label,
                hierarchy_path=[case_name, citation, label.title()],
                metadata={"citation": citation, "case_name": case_name},
            ))
    return chunks


def chunk_freeform(text: str, *, source: str, max_tokens: int = 800) -> list[Chunk]:
    """Generic chunker for company docs / treatises — paragraph-based with cap."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[Chunk] = []
    buf: list[str] = []
    buf_tok = 0
    for para in paragraphs:
        ptok = max(1, len(para) // 4)
        if buf and buf_tok + ptok > max_tokens:
            chunks.append(Chunk(text="\n\n".join(buf), chunk_type="paragraph",
                                  hierarchy_path=[source], metadata={"source": source}))
            buf, buf_tok = [], 0
        buf.append(para)
        buf_tok += ptok
    if buf:
        chunks.append(Chunk(text="\n\n".join(buf), chunk_type="paragraph",
                              hierarchy_path=[source], metadata={"source": source}))
    return chunks


# ---------- Helpers ----------

def _split_by_tokens(text: str, max_tokens: int) -> list[str]:
    if max(1, len(text) // 4) <= max_tokens:
        return [text]
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    out: list[str] = []
    cur: list[str] = []
    cur_tok = 0
    for p in paragraphs:
        ptok = max(1, len(p) // 4)
        if cur and cur_tok + ptok > max_tokens:
            out.append("\n\n".join(cur))
            cur, cur_tok = [], 0
        cur.append(p)
        cur_tok += ptok
    if cur:
        out.append("\n\n".join(cur))
    return out or [text]


def _looks_like_subsection(num: str) -> bool:
    """A bare-section regex match like '(1)' should not start a new section."""
    return bool(re.match(r"^\(\d+\)$", num))
