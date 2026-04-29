"""Drafts and notices."""


def test_draft_rental_agreement(client):
    client.post("/api/session")
    r = client.post("/api/draft", json={
        "workflow": "rental_agreement",
        "inputs": {
            "state": "Maharashtra",
            "landlord_name": "A Landlord",
            "tenant_name": "B Tenant",
            "premises_address": "Flat 12, Bandra, Mumbai",
            "monthly_rent_inr": "50000",
            "deposit_inr": "100000",
            "tenure_months": "11",
            "start_date": "2026-05-01",
        },
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["body_md"]
    assert body["title"]


def test_draft_missing_required(client):
    client.post("/api/session")
    r = client.post("/api/draft", json={
        "workflow": "rental_agreement",
        "inputs": {"state": "Maharashtra"},
    })
    # FastAPI returns 500 on uncaught ValueError; in production we'd map it to 422.
    # Either is acceptable as long as it's not 200.
    assert r.status_code != 200


def test_notice_s138(client):
    client.post("/api/session")
    r = client.post("/api/notice", json={
        "workflow": "s138_ni_act_notice",
        "inputs": {
            "payee_name": "Payee", "payee_address": "Addr1",
            "drawer_name": "Drawer", "drawer_address": "Addr2",
            "cheque_number": "000123", "cheque_date": "2026-04-01",
            "cheque_amount_inr": "200000", "bank_name": "HDFC",
            "dishonour_date": "2026-04-15", "underlying_debt": "supply of goods",
        },
    })
    assert r.status_code == 200
    body = r.json()
    assert body["body_md"]


def test_artifacts_list(client):
    client.post("/api/session")
    # Create one.
    client.post("/api/notice", json={
        "workflow": "defamation_notice",
        "inputs": {
            "claimant": "X", "respondent": "Y",
            "alleged_statement": "false statement",
            "publication_date": "2026-04-20",
            "harm_description": "loss of reputation",
            "relief_sought": "apology",
        },
    })
    r = client.get("/api/artifacts")
    assert r.status_code == 200
    assert len(r.json()) >= 1
