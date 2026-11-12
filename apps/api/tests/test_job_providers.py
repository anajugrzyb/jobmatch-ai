from datetime import UTC

from app.modules.jobs.providers import (
    normalize_arbeitnow,
    normalize_remotive,
    parse_date,
    plain_text,
)


def test_remotive_normalization():
    item = {
        "id": 42, "title": "Python Developer", "company_name": "Acme",
        "url": "https://example.org/job/42",
        "description": "<p>Python &amp; SQL</p>",
        "candidate_required_location": "Worldwide",
        "tags": ["Python", "SQL"],
        "publication_date": "2026-11-01T10:00:00",
    }
    job = normalize_remotive(item)
    assert job is not None
    assert job.source_id == "42"
    assert job.remote is True
    assert job.description == "Python & SQL"
    assert job.published_at is not None
    assert job.published_at.tzinfo is not None


def test_arbeitnow_normalization():
    item = {
        "slug": "python-role", "title": "Python Developer", "company_name": "Acme",
        "url": "https://example.org/job/python",
        "description": "Backend", "location": "Berlin",
        "remote": False, "tags": ["Python"], "created_at": 1762000000,
    }
    job = normalize_arbeitnow(item)
    assert job is not None
    assert job.source == "arbeitnow"
    assert job.remote is False
    assert job.published_at is not None


def test_invalid_records_are_skipped():
    assert normalize_remotive({"id": 1, "title": "Broken", "url": "not-a-url"}) is None
    assert normalize_arbeitnow({}) is None


def test_html_and_date_handling():
    assert plain_text("<b>SQL</b> &amp; Python") == "SQL & Python"
    assert parse_date("invalid") is None
    assert parse_date("2026-11-01T10:00:00Z").tzinfo == UTC
