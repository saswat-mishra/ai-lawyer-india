"""Device-ID session: signed cookie, no auth.

A new device gets a UUID v4. The cookie is signed with itsdangerous to prevent
client tampering — the device_id is the trust boundary for company KB isolation
so accepting an arbitrary client-supplied UUID would let any client read any
device's docs. Signing closes that hole.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Request, Response
from itsdangerous import BadSignature, TimestampSigner

from app.core.config import get_settings


def _signer() -> TimestampSigner:
    return TimestampSigner(get_settings().device_cookie_secret, salt="device-id")


def make_signed(device_id: str) -> str:
    return _signer().sign(device_id).decode("utf-8")


def parse_signed(signed: str) -> str | None:
    settings = get_settings()
    max_age = settings.device_cookie_max_age_days * 24 * 3600
    try:
        return _signer().unsign(signed, max_age=max_age).decode("utf-8")
    except BadSignature:
        return None


def get_or_create_device_id(request: Request, response: Response) -> str:
    """Return current device_id (creating a new one + setting cookie if absent).

    Idempotent on repeat calls within the same request because we set the cookie
    on the *response* and read from the request once.
    """
    settings = get_settings()
    raw = request.cookies.get(settings.device_cookie_name)
    if raw:
        device_id = parse_signed(raw)
        if device_id:
            return device_id

    device_id = str(uuid.uuid4())
    signed = make_signed(device_id)
    response.set_cookie(
        key=settings.device_cookie_name,
        value=signed,
        max_age=settings.device_cookie_max_age_days * 24 * 3600,
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
        path="/",
    )
    return device_id


def device_id_from_request(request: Request) -> str | None:
    """Read-only fetch of device_id (e.g., for streaming endpoints).

    If the device hasn't been created yet, the caller must establish a session
    via POST /api/session first.
    """
    settings = get_settings()
    raw = request.cookies.get(settings.device_cookie_name)
    if not raw:
        return None
    return parse_signed(raw)
