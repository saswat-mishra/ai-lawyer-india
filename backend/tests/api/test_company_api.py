"""Company KB API."""
import io


def _txt(name="x.txt", content=b"hello world"):
    return ("file", (name, io.BytesIO(content), "text/plain"))


def test_upload_then_list(client):
    client.post("/api/session")
    r = client.post("/api/company/docs", files=[_txt("a.txt", b"my company contract")],
                      data={"doc_type": "agreement"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] in {"ready", "uploaded"}
    r2 = client.get("/api/company/docs")
    assert any(d["id"] == body["id"] for d in r2.json())


def test_unsupported_mime_rejected(client):
    client.post("/api/session")
    r = client.post(
        "/api/company/docs",
        files=[("file", ("evil.exe", io.BytesIO(b"MZ"), "application/x-dosexec"))],
        data={"doc_type": "agreement"},
    )
    assert r.status_code == 415


def test_oversize_rejected(client, monkeypatch):
    client.post("/api/session")
    # Patch the limit low to avoid actually allocating 50MB.
    from app.api import routes_company
    monkeypatch.setattr(routes_company, "MAX_BYTES", 16)
    r = client.post(
        "/api/company/docs",
        files=[_txt("big.txt", b"X" * 32)],
        data={"doc_type": "agreement"},
    )
    assert r.status_code == 413


def test_cross_device_isolation(client):
    client.post("/api/session")
    r = client.post("/api/company/docs", files=[_txt("a.txt", b"device A doc")],
                      data={"doc_type": "agreement"})
    a_id = r.json()["id"]
    # Switch device.
    client.cookies.clear()
    client.post("/api/session")
    r2 = client.get("/api/company/docs")
    assert all(d["id"] != a_id for d in r2.json())


def test_delete(client):
    client.post("/api/session")
    r = client.post("/api/company/docs", files=[_txt("a.txt", b"to delete")],
                      data={"doc_type": "agreement"})
    doc_id = r.json()["id"]
    r2 = client.delete(f"/api/company/docs/{doc_id}")
    assert r2.status_code == 200
    r3 = client.get("/api/company/docs")
    assert all(d["id"] != doc_id for d in r3.json())
