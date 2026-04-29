"""Citation faithfulness harness.

The keystone test. We feed the verifier deliberately-mixed inputs (real
citations + fabricated citations) and assert that:

1. Every fabricated citation is flagged as unverified.
2. After `strip_unverified`, no fabricated citation tokens remain in the
   user-facing text.
3. Every real citation passes verification.

This runs without OpenAI: it does not depend on a model — it tests the
verifier directly against the seeded corpus.
"""
import json
import pytest

from app.verify.citations import Citation, parse_citations, strip_unverified, verify_citations


# (text, expected_real_count, expected_fake_count)
FIXTURES = [
    (
        "Murder is punished under Section 103 BNS. The earlier Section 9999 BNS does not exist.",
        1, 1,
    ),
    (
        "See AIR 1986 SC 180 for the right to livelihood. There is no AIR 9999 SC 9999.",
        1, 1,
    ),
    (
        "Section 138 NI Act and Section 73 of the Indian Contract Act both apply.",
        2, 0,
    ),
    (
        "Per Section 420 IPC and the fictional Section 12345 of the Made-Up Act.",
        # IPC §420 is in the seed corpus (real); 'Made-Up Act' parses but doesn't
        # exist in the corpus, so it's correctly flagged as unverified.
        1, 1,
    ),
    (
        "Bogus citation: Section 7777 BNS, Section 8888 NI Act.",
        0, 2,
    ),
]


@pytest.mark.parametrize("text,real_count,fake_count", FIXTURES)
@pytest.mark.asyncio
async def test_verifier_strips_fakes(seeded, text, real_count, fake_count):
    parsed = parse_citations(text)
    res = await verify_citations(parsed)
    assert len(res.verified) == real_count, (
        f"expected {real_count} verified, got {len(res.verified)}: {res.verified}")
    assert len(res.unverified) == fake_count, (
        f"expected {fake_count} unverified, got {len(res.unverified)}")

    # After stripping, nothing fabricated should remain in the body.
    cleaned = strip_unverified(text, res)
    for fake in res.unverified:
        assert fake.raw not in cleaned, (
            f"fabricated citation {fake.raw!r} survived stripping")


@pytest.mark.asyncio
async def test_full_pipeline_strips_fakes(seeded, client):
    """Run the live agent and assert that any unverified citations are removed
    from the user-facing answer.
    """
    client.post("/api/session")
    r = client.post("/api/chat", json={"query": "Tell me about Section 103 BNS and Section 9999 BNS"})
    body = r.json()
    # Mock answer cites real sections; if it ever cites a fake one, the verifier
    # must strip it. Assert: nothing in the final answer references "9999".
    assert "9999" not in body["answer_md"], body["answer_md"]
