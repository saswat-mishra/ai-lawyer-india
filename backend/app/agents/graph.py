"""Top-level agent runner. Linear pipeline with one branch (clarify -> stop)."""
from __future__ import annotations

from app.agents.nodes import classify, clarify, finalize, retrieve, synthesize, verify
from app.agents.state import AgentState
from app.core.config import Persona
from app.db import store


async def run_agent(*, device_id: str, conversation_id: str | None,
                     query: str, slots: dict | None = None) -> AgentState:
    device = await store.get_device(device_id) or await store.upsert_device(device_id)
    persona = Persona(device.get("persona", "citizen"))
    state = AgentState(
        device_id=device_id,
        conversation_id=conversation_id,
        persona=persona,
        language_pref=device.get("language_pref", "en"),
        user_query=query,
        slots=slots or {},
    )
    if conversation_id:
        await store.add_message(conversation_id, role="user", content=query,
                                  meta={"slots": slots or {}})

    state = await classify(state)
    state = await clarify(state)
    if state.needs_clarification:
        # Persist a clarification message so the conversation thread keeps it.
        if conversation_id:
            await store.add_message(conversation_id, role="clarification",
                                      content="awaiting user input",
                                      meta={"questions": state.clarifying_questions})
        return state

    state = await retrieve(state)
    state = await synthesize(state)
    state = await verify(state)
    state = await finalize(state)
    return state
