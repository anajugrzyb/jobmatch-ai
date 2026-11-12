"""Public job feeds. No scraping, browser automation or credentials required."""
from datetime import datetime, timezone
import re
from html import unescape

import httpx

from app.modules.jobs.schemas import NormalizedJob

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"
ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"
MAX_RESULTS = 100
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
HEADERS = {"User-Agent": "JobMatchAI/0.3 (personal local job discovery)"}


def plain_text(value: object) -> str:
    text = str(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def parse_date(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result
    except ValueError:
        return None


def normalize_remotive(item: dict) -> NormalizedJob | None:
    try:
        return NormalizedJob(
            source="remotive",
            source_id=str(item["id"]),
            title=str(item["title"])[:200],
            company=str(item.get("company_name") or "Não informada")[:200],
            source_url=item["url"],
            description=plain_text(item.get("description"))[:12000],
            location=str(item.get("candidate_required_location") or "Remoto")[:200],
            remote=True,
            tags=", ".join(str(tag) for tag in item.get("tags", []) if isinstance(tag, str))[:1000],
            published_at=parse_date(item.get("publication_date")),
        )
    except (KeyError, ValueError, TypeError):
        return None


def normalize_arbeitnow(item: dict) -> NormalizedJob | None:
    try:
        return NormalizedJob(
            source="arbeitnow",
            source_id=str(item["slug"])[:160],
            title=str(item["title"])[:200],
            company=str(item.get("company_name") or "Não informada")[:200],
            source_url=item["url"],
            description=plain_text(item.get("description"))[:12000],
            location=str(item.get("location") or "")[:200],
            remote=bool(item.get("remote", False)),
            tags=", ".join(str(tag) for tag in item.get("tags", []) if isinstance(tag, str))[:1000],
            published_at=datetime.fromtimestamp(item["created_at"], tz=timezone.utc)
            if isinstance(item.get("created_at"), (int, float)) else None,
        )
    except (KeyError, ValueError, TypeError, OverflowError, OSError):
        return None


async def fetch_jobs(source: str, query: str = "") -> list[NormalizedJob]:
    if source not in ("remotive", "arbeitnow"):
        raise ValueError("Fonte não suportada")
    url = REMOTIVE_URL if source == "remotive" else ARBEITNOW_URL
    params = {"search": query} if source == "remotive" and query else {}
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(15.0),
        follow_redirects=False,
        headers=HEADERS,
    ) as client:
        async with client.stream("GET", url, params=params) as response:
            response.raise_for_status()
            data = bytearray()
            async for chunk in response.aiter_bytes():
                data.extend(chunk)
                if len(data) > MAX_RESPONSE_BYTES:
                    raise ValueError("Resposta da fonte excedeu o limite de tamanho")
    import json
    payload = json.loads(data)
    if not isinstance(payload, dict) or not isinstance(payload.get("jobs" if source == "remotive" else "data"), list):
        raise ValueError("Formato inesperado da fonte")
    records = payload["jobs" if source == "remotive" else "data"][:MAX_RESULTS]
    normalize = normalize_remotive if source == "remotive" else normalize_arbeitnow
    jobs = [normalize(item) for item in records if isinstance(item, dict)]
    return [job for job in jobs if job is not None]
