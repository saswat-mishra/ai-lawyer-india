"""IPC -> BNS lookup."""
import pytest
from datetime import date

from app.verify.successor import applies_old_law, successor_for


@pytest.mark.asyncio
async def test_ipc_302_maps_to_bns_103(seeded):
    m = await successor_for("IPC", "302")
    assert m is not None
    assert m["new_act"] == "BNS"
    assert m["new_section"] == "103"


@pytest.mark.asyncio
async def test_unknown_returns_none(seeded):
    assert await successor_for("IPC", "9999") is None


def test_temporal_regime():
    assert applies_old_law(date(2024, 6, 30)) is True
    assert applies_old_law(date(2024, 7, 1)) is False
    assert applies_old_law(date(2025, 1, 1)) is False
    assert applies_old_law(None) is False
