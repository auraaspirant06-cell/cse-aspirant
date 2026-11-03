"""
Integration Tests for NextGen FastAPI Endpoints
"""
import os
import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)
MASTER_API_KEY = os.environ["MASTER_API_KEY"]

def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "system" in data

def test_metrics_prometheus():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "cse_aspirant_commands_total" in res.text

def test_api_keys_and_access():
    # 1. Generate new API key using Master Owner Key
    gen_res = client.post(
        "/api/v1/keys/generate",
        headers={"X-API-Key": MASTER_API_KEY},
        json={"user_id": 101, "tier": "PRO"}
    )
    assert gen_res.status_code == 200
    new_key = gen_res.json()["data"]["key"]
    assert new_key.startswith("csea_pro_")

    # 2. Use the generated key on music play endpoint
    play_res = client.post(
        "/api/v1/music/play",
        headers={"X-API-Key": new_key},
        json={"chat_id": 555, "query_or_url": "Coding Ambient Beats", "requester_id": 101}
    )
    assert play_res.status_code == 200
    assert play_res.json()["success"] is True

    # 3. Revoke key
    revoke_res = client.post(
        "/api/v1/keys/revoke",
        headers={"X-API-Key": MASTER_API_KEY},
        json={"key": new_key}
    )
    assert revoke_res.status_code == 200

    # 4. Attempting to use revoked key must fail with 401
    bad_res = client.post(
        "/api/v1/music/play",
        headers={"X-API-Key": new_key},
        json={"chat_id": 555, "query_or_url": "Song", "requester_id": 101}
    )
    assert bad_res.status_code == 401

def test_education_endpoints():
    res = client.get("/api/v1/education/summary?lang=en")
    assert res.status_code == 200
    assert res.json()["success"] is True

    cs_res = client.get("/api/v1/education/cs/os?lang=en")
    assert cs_res.status_code == 200
    assert "Operating Systems" in cs_res.json()["data"]["overview"]

def test_payment_endpoints():
    # Invoice
    inv_res = client.get("/api/v1/payments/invoice/99?plan=PREMIUM&amount=199")
    assert inv_res.status_code == 200
    assert "upi_intent" in inv_res.json()["data"]

    # Submission
    sub_res = client.post(
        "/api/v1/payments/submit",
        json={"user_id": 99, "utr": "UTRAPI123456", "amount": 199.0, "method": "UPI"}
    )
    assert sub_res.status_code == 200
    assert sub_res.json()["data"]["status"] == "PENDING"

