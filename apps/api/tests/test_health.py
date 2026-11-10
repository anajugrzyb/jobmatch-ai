from fastapi.testclient import TestClient
from app.main import app


def test_health():
    response = TestClient(app).get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "jobmatch-api"}


def test_openapi():
    response = TestClient(app).get("/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/health" in response.json()["paths"]
