import sys, os, importlib, json
sys.path.append(os.path.abspath("."))
from fastapi.testclient import TestClient

TOKEN = "secret"
os.environ["WEB_TOKEN"] = TOKEN


def get_client():
    import receipt_relay.config as config
    import receipt_relay.web.main as web
    importlib.reload(config)
    importlib.reload(web)
    return TestClient(web.app), config


def test_index():
    client, _ = get_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Receipt Relay Test" in resp.text


def test_print_text():
    client, _ = get_client()
    resp = client.post("/print", data={"text": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "job_id" in data


def test_config_requires_token():
    client, _ = get_client()
    resp = client.get("/config")
    assert resp.status_code == 401


def test_config_load_and_update():
    client, config = get_client()
    headers = {"X-Token": TOKEN}

    resp = client.get("/config", headers=headers)
    assert resp.status_code == 200
    assert "SIGNAL_NUMBER" in resp.text

    resp = client.post(
        "/config",
        headers=headers,
        data={
            "signal_number": "+15551234567",
            "allowed_senders": "+15550001111",
            "signal_rest_url": "http://example.com",
        },
    )
    assert resp.status_code == 200
    assert config.CONFIG_PATH.exists()
    data = json.loads(config.CONFIG_PATH.read_text())
    assert data["signal_number"] == "+15551234567"
    assert config.settings.signal_number == "+15551234567"
    config.CONFIG_PATH.unlink()

