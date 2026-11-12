from fastapi.testclient import TestClient

from app.main import app


def test_invalid_source_is_rejected():
    response = TestClient(app).post("/api/v1/jobs/import", json={"source": "unknown"})
    assert response.status_code == 422


def test_invalid_query_length_is_rejected():
    response = TestClient(app).get("/api/v1/jobs", params={"q": "x" * 101})
    assert response.status_code == 422


def test_invalid_pagination_is_rejected():
    response = TestClient(app).get("/api/v1/jobs", params={"limit": 101})
    assert response.status_code == 422
