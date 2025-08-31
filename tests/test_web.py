import sys, os
sys.path.append(os.path.abspath("."))
from fastapi.testclient import TestClient
from receipt_relay.web.main import app


def test_index():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Receipt Relay Test" in resp.text


def test_print_text():
    client = TestClient(app)
    resp = client.post("/print", data={"text": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "job_id" in data
