"""Session routes — device-ID issue + persona/language settings."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response

from app.api.schemas import (LanguageUpdateRequest, PersonaUpdateRequest,
                                SessionResponse)
from app.core.device import device_id_from_request, get_or_create_device_id
from app.db import store

router = APIRouter(prefix="/api/session", tags=["session"])


@router.post("", response_model=SessionResponse)
async def get_or_create_session(request: Request, response: Response) -> SessionResponse:
    device_id = get_or_create_device_id(request, response)
    device = await store.upsert_device(device_id)
    return SessionResponse(
        device_id=device["device_id"],
        persona=device["persona"],
        language_pref=device["language_pref"],
    )


@router.patch("/persona", response_model=SessionResponse)
async def set_persona(req: PersonaUpdateRequest, request: Request,
                       response: Response) -> SessionResponse:
    device_id = get_or_create_device_id(request, response)
    device = await store.update_device_persona(device_id, req.persona)
    return SessionResponse(
        device_id=device["device_id"],
        persona=device["persona"],
        language_pref=device["language_pref"],
    )


@router.patch("/language", response_model=SessionResponse)
async def set_language(req: LanguageUpdateRequest, request: Request,
                        response: Response) -> SessionResponse:
    device_id = get_or_create_device_id(request, response)
    device = await store.update_device_language(device_id, req.language_pref)
    return SessionResponse(
        device_id=device["device_id"],
        persona=device["persona"],
        language_pref=device["language_pref"],
    )


@router.get("/me", response_model=SessionResponse)
async def me(request: Request) -> SessionResponse:
    device_id = device_id_from_request(request)
    if not device_id:
        raise HTTPException(401, "no session — call POST /api/session first")
    device = await store.get_device(device_id)
    if not device:
        raise HTTPException(401, "device unknown")
    return SessionResponse(**{
        "device_id": device["device_id"],
        "persona": device["persona"],
        "language_pref": device["language_pref"],
    })
