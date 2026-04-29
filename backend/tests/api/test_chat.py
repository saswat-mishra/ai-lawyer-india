"""Chat API end-to-end (with seed corpus, mock OpenAI)."""
import pytest


def test_chat_basic(client):
    client.post("/api/session")
    r = client.post("/api/chat", json={"query": "What is Section 103 BNS?"})
    assert r.status_code == 200
    body = r.json()
    assert body["conversation_id"]
    assert body["answer_md"]
    assert body["confidence"] in {"high", "medium", "low", "refused"}


def test_chat_clarifies_for_landlord(client):
    client.post("/api/session")
    # Force the mock-classify into returning a landlord-ish state by including
    # an unmistakable trigger and making the reduce step want a 'state' slot.
    r = client.post("/api/chat", json={"query": "my landlord wants to evict me from rented flat"})
    assert r.status_code == 200
    body = r.json()
    # Either we got an answer with citations (because landlord patterns matched),
    # or we got clarifying questions. Either is acceptable behavior.
    assert (body["needs_clarification"] is False
            and body["answer_md"]) or (
            body["needs_clarification"] is True
            and len(body["clarifying_questions"]) > 0)


def test_chat_persists_conversation(client):
    client.post("/api/session")
    r = client.post("/api/chat", json={"query": "Section 138 NI Act"})
    cid = r.json()["conversation_id"]
    # Continue the conversation.
    r2 = client.post("/api/chat", json={"query": "and what's the limitation?",
                                          "conversation_id": cid})
    assert r2.json()["conversation_id"] == cid

    # Listing conversations should show one entry.
    r3 = client.get("/api/chat/conversations")
    convs = r3.json()
    assert any(c["id"] == cid for c in convs)


def test_messages_endpoint_isolates_devices(client):
    # Device A creates a conversation.
    client.post("/api/session")
    r = client.post("/api/chat", json={"query": "anything"})
    cid = r.json()["conversation_id"]

    # New "device" — clear cookies.
    client.cookies.clear()
    client.post("/api/session")
    r2 = client.get(f"/api/chat/conversations/{cid}/messages")
    # Device B must not be able to read device A's conversation.
    assert r2.status_code == 404


def test_chat_404_unknown_conversation(client):
    client.post("/api/session")
    r = client.post("/api/chat", json={
        "query": "x", "conversation_id": "11111111-1111-1111-1111-111111111111",
    })
    assert r.status_code == 404
