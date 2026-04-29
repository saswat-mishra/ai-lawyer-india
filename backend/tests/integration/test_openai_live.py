"""Live OpenAI smoke tests. Skipped unless OPENAI_API_KEY is set in env."""
import os

import pytest


pytestmark = pytest.mark.openai


def _has_key() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


@pytest.mark.skipif(not _has_key(), reason="OPENAI_API_KEY not set")
@pytest.mark.asyncio
async def test_real_embedding_dimensions():
    from app.core.config import get_settings
    get_settings.cache_clear()  # type: ignore[attr-defined]
    from app.llm.openai_client import embed
    out = await embed(["What is Section 138 of the Negotiable Instruments Act?"])
    assert len(out) == 1
    assert len(out[0]) == 1536
    # Real embeddings have varied magnitude, not the deterministic mock pattern.
    assert any(x != 0.0 for x in out[0])


@pytest.mark.skipif(not _has_key(), reason="OPENAI_API_KEY not set")
@pytest.mark.asyncio
async def test_real_chat_round_trip():
    from app.core.config import get_settings
    get_settings.cache_clear()  # type: ignore[attr-defined]
    from app.llm.openai_client import ChatMessage, chat_complete
    out = await chat_complete(
        [
            ChatMessage("system",
                          "You are a curt assistant. Reply with exactly: OK"),
            ChatMessage("user", "Say OK"),
        ],
        temperature=0.0, max_tokens=10,
    )
    assert "OK" in out


@pytest.mark.skipif(not _has_key(), reason="OPENAI_API_KEY not set")
@pytest.mark.asyncio
async def test_real_agent_finds_section_103(seeded):
    """Real embeddings should produce meaningful retrieval; mock embedder didn't."""
    from app.core.config import get_settings
    get_settings.cache_clear()  # type: ignore[attr-defined]
    from app.agents.graph import run_agent
    state = await run_agent(device_id="d-live", conversation_id=None,
                              query="What is the punishment for murder under Indian law?")
    assert state.legal_results, "expected retrievals from real embedding"
    sections = [c.section_number for c in state.legal_results]
    # BNS §103 (current law) should be in the top results.
    assert "103" in sections
