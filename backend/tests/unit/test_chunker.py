"""Chunker correctness on small statute and case fixtures."""
from app.rag.chunker import chunk_case, chunk_freeform, chunk_statute


SAMPLE_STATUTE = """
Chapter VI Of Offences Affecting the Human Body

Section 100. Culpable homicide.—Whoever causes death by doing an act with the
intention of causing death, or with the intention of causing such bodily injury
as is likely to cause death, or with the knowledge that he is likely by such
act to cause death, commits the offence of culpable homicide.

Section 103. Punishment for murder.—(1) Whoever commits murder shall be
punished with death or imprisonment for life, and shall also be liable to fine.
(2) When a group of five or more persons acting in concert commits murder...
each member of such group shall be punished with death or with imprisonment
for life, and shall also be liable to fine.

Provided that nothing herein shall apply to lawful acts.
"""


def test_chunk_statute_section_boundaries():
    chunks = chunk_statute(SAMPLE_STATUTE, act_short="BNS",
                            act_title="Bharatiya Nyaya Sanhita, 2023")
    section_numbers = [c.section_number for c in chunks if c.chunk_type == "section"]
    assert "100" in section_numbers
    assert "103" in section_numbers
    s103 = next(c for c in chunks if c.section_number == "103")
    # Subsection (1) and (2) and proviso must roll into the parent.
    assert "(1)" in s103.text and "(2)" in s103.text
    assert "Provided that" in s103.text
    # Hierarchy must include the chapter.
    assert any("Chapter" in p for p in s103.hierarchy_path)


SAMPLE_CASE = """
HEADNOTE
Right to livelihood is part of right to life.

FACTS
The petitioners were pavement dwellers...

ISSUES
Whether eviction without notice violates Article 21.

HELD
Article 21 includes the right to livelihood.

RATIO
Procedural due process requires notice and hearing before eviction.
"""


def test_chunk_case_anchors():
    chunks = chunk_case(SAMPLE_CASE, citation="AIR 1986 SC 180",
                          case_name="Olga Tellis v. BMC")
    types = {c.chunk_type for c in chunks}
    assert "headnote" in types
    assert "held" in types
    assert "ratio" in types
    held = next(c for c in chunks if c.chunk_type == "held")
    assert "Article 21" in held.text


def test_chunk_freeform_paragraph_caps():
    text = ("para one " * 200 + "\n\n" + "para two " * 50)
    chunks = chunk_freeform(text, source="doc", max_tokens=100)
    assert len(chunks) >= 2
    assert all(c.text for c in chunks)
