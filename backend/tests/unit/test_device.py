"""Device-ID signing + parsing."""
from app.core.device import make_signed, parse_signed


def test_round_trip():
    raw = "11111111-2222-3333-4444-555555555555"
    signed = make_signed(raw)
    assert signed != raw
    assert parse_signed(signed) == raw


def test_tampered_rejected():
    raw = "abc"
    signed = make_signed(raw)
    # Replace separator with a char outside base64-urlsafe alphabet — guaranteed invalid.
    tampered = signed.replace(".", "@", 1)
    assert parse_signed(tampered) is None
    # Also: flipping the value half before the timestamp must fail.
    tampered2 = "xyz" + signed[3:]
    assert parse_signed(tampered2) is None


def test_garbage_rejected():
    assert parse_signed("garbage") is None
    assert parse_signed("") is None
