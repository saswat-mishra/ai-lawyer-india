"""Verify the deterministic mock OpenAI wrapper behaves correctly without a key."""
import pytest

from app.llm.openai_client import ChatMessage, chat_complete, embed


@pytest.mark.asyncio
async def test_embed_deterministic():
    a1 = await embed(["hello"])
    a2 = await embed(["hello"])
    assert a1 == a2
    assert len(a1[0]) == 1536


@pytest.mark.asyncio
async def test_embed_different_inputs_yield_different_vectors():
    a = await embed(["hello"])
    b = await embed(["world"])
    assert a != b


@pytest.mark.asyncio
async def test_classify_returns_json():
    out = await chat_complete([ChatMessage("system", "classify"),
                                  ChatMessage("user", "I need help with a murder case")],
                                 response_format="json")
    import json
    data = json.loads(out)
    assert "category" in data
    assert data["category"] == "criminal"


@pytest.mark.asyncio
async def test_clarify_for_landlord_query():
    out = await chat_complete([ChatMessage("system", "clarify missing information"),
                                  ChatMessage("user", "my landlord wants to evict me")],
                                 response_format="json")
    import json
    data = json.loads(out)
    assert "questions" in data
    slots = {q["slot"] for q in data["questions"]}
    assert "state" in slots


@pytest.mark.asyncio
async def test_synthesize_general_response():
    out = await chat_complete([ChatMessage("system", "answer"),
                                  ChatMessage("user", "what is section 138 NI Act?")],
                                 response_format=None)
    assert "138" in out
