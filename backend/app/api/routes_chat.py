"""Chat routes. JSON for full responses; SSE for streaming."""
from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import StreamingResponse

from app.agents.graph import run_agent
from app.api.schemas import (ChatRequest, ChatResponse, CitationOut,
                                ConversationOut, MessageOut)
from app.core.device import device_id_from_request, get_or_create_device_id
from app.db import store

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request, response: Response) -> ChatResponse:
    device_id = get_or_create_device_id(request, response)
    conv_id = req.conversation_id
    if not conv_id:
        conv = await store.create_conversation(device_id, title=_title_from_query(req.query))
        conv_id = conv["id"]
    else:
        conv = await store.get_conversation(conv_id, device_id)
        if not conv:
            raise HTTPException(404, "conversation not found")

    state = await run_agent(device_id=device_id, conversation_id=conv_id,
                              query=req.query, slots=req.slots)

    return ChatResponse(
        conversation_id=conv_id,
        answer_md=state.answer_md,
        citations=[CitationOut(**c.to_dict()) for c in state.citations],
        confidence=state.confidence,
        refused=state.refused,
        refusal_reason=state.refusal_reason,
        needs_clarification=state.needs_clarification,
        clarifying_questions=state.clarifying_questions,
        trace=state.trace,
    )


@router.post("/stream")
async def chat_stream(req: ChatRequest, request: Request, response: Response):
    device_id = get_or_create_device_id(request, response)
    conv_id = req.conversation_id
    if not conv_id:
        conv = await store.create_conversation(device_id, title=_title_from_query(req.query))
        conv_id = conv["id"]
    else:
        conv = await store.get_conversation(conv_id, device_id)
        if not conv:
            raise HTTPException(404, "conversation not found")

    async def event_stream() -> AsyncIterator[str]:
        # Stage 1: classify (emit step).
        yield _sse("stage", {"step": "classify"})
        state = await run_agent(device_id=device_id, conversation_id=conv_id,
                                  query=req.query, slots=req.slots)
        # We emit the full structured response in one event after the agent finishes;
        # the frontend can also subscribe to incremental chat_stream once we wire
        # token-level streaming through the synthesize node. For now, this is the
        # single-shot SSE form, sufficient for the UX (show stage spinners + final).
        if state.needs_clarification:
            yield _sse("clarify", {"questions": state.clarifying_questions})
            yield _sse("done", {"conversation_id": conv_id})
            return
        yield _sse("answer", {
            "answer_md": state.answer_md,
            "citations": [c.to_dict() for c in state.citations],
            "confidence": state.confidence,
            "refused": state.refused,
            "refusal_reason": state.refusal_reason,
        })
        yield _sse("done", {"conversation_id": conv_id})

    return StreamingResponse(event_stream(), media_type="text/event-stream",
                                headers={"Cache-Control": "no-cache",
                                          "X-Accel-Buffering": "no"})


@router.get("/conversations", response_model=list[ConversationOut])
async def list_conversations(request: Request) -> list[ConversationOut]:
    device_id = device_id_from_request(request)
    if not device_id:
        return []
    convs = await store.list_conversations(device_id)
    return [ConversationOut(**{
        "id": c["id"], "title": c["title"], "workflow": c["workflow"],
        "updated_at": c["updated_at"],
    }) for c in convs]


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageOut])
async def get_messages(conversation_id: str, request: Request) -> list[MessageOut]:
    device_id = device_id_from_request(request)
    if not device_id:
        raise HTTPException(401, "no session")
    conv = await store.get_conversation(conversation_id, device_id)
    if not conv:
        raise HTTPException(404, "conversation not found")
    msgs = await store.list_messages(conversation_id)
    return [MessageOut(**m) for m in msgs]


def _title_from_query(q: str) -> str:
    return (q[:60] + "...") if len(q) > 60 else q


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
