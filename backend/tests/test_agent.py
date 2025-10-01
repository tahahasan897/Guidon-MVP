from fastapi.testclient import TestClient
from app.main import app


def test_run_agent():
    client = TestClient(app)
    r = client.post("/api/agent/run", json={"goal": "test", "mode": "on_demand"})
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "queued"
    assert body.get("run_id")
