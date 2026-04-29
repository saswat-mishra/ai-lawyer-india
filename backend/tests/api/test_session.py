"""Session API: device-ID issuance, persistence, persona update."""


def test_session_creates_cookie(client):
    r = client.post("/api/session")
    assert r.status_code == 200
    body = r.json()
    assert body["persona"] == "citizen"
    assert "ail_did" in r.cookies


def test_session_returns_existing_device(client):
    r1 = client.post("/api/session")
    did1 = r1.json()["device_id"]
    r2 = client.post("/api/session")
    did2 = r2.json()["device_id"]
    assert did1 == did2


def test_persona_update(client):
    client.post("/api/session")
    r = client.patch("/api/session/persona", json={"persona": "founder"})
    assert r.status_code == 200
    assert r.json()["persona"] == "founder"


def test_persona_invalid(client):
    client.post("/api/session")
    r = client.patch("/api/session/persona", json={"persona": "wizard"})
    assert r.status_code == 422


def test_me_requires_session(client):
    r = client.get("/api/session/me")
    assert r.status_code == 401
