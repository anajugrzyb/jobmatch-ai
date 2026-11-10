from fastapi.testclient import TestClient

from app.main import app


def test_profile_validation_rejects_oversized_name():
    response = TestClient(app).put("/api/v1/profile", json={"full_name": "a" * 161})
    assert response.status_code == 422


def test_resume_rejects_invalid_content_type():
    response = TestClient(app).post(
        "/api/v1/resume/extract",
        files={"file": ("resume.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_resume_rejects_large_file():
    response = TestClient(app).post(
        "/api/v1/resume/extract",
        files={"file": ("resume.pdf", b"%PDF-" + b"x" * (5 * 1024 * 1024), "application/pdf")},
    )
    assert response.status_code == 413
