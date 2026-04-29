"""IPC -> BNS / CrPC -> BNSS / Evidence -> BSA mapping helper.

Used (a) to surface the new section when a user cites the old one, and
(b) to remind the user that BNS applies only to offences on/after 1 Jul 2024.
"""
from __future__ import annotations

from datetime import date
from app.db import store

BNS_EFFECTIVE = date(2024, 7, 1)


async def successor_for(old_act: str, old_section: str) -> dict | None:
    return await store.lookup_successor_section(old_act, old_section)


def applies_old_law(incident_date: date | None) -> bool:
    """Returns True if the IPC/CrPC/Evidence Act regime governs this incident."""
    if incident_date is None:
        return False  # Unknown -> caller should ask via clarification
    return incident_date < BNS_EFFECTIVE
