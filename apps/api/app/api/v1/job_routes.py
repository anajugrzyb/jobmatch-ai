from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import literal_column, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
import httpx

from app.db.session import SessionLocal
from app.modules.jobs.models import Job
from app.modules.jobs.providers import fetch_jobs
from app.modules.jobs.schemas import ImportRequest, ImportResponse, JobResponse

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


@router.get("", response_model=list[JobResponse])
def list_jobs(
    q: str = Query(default="", max_length=100),
    location: str = Query(default="", max_length=100),
    remote_only: bool = False,
    source: str | None = Query(default=None, pattern="^(remotive|arbeitnow)$"),
    limit: int = Query(default=30, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    stmt = select(Job)
    if q.strip():
        term = f"%{q.strip()}%"
        stmt = stmt.where(or_(Job.title.ilike(term), Job.company.ilike(term), Job.tags.ilike(term)))
    if location.strip():
        stmt = stmt.where(Job.location.ilike(f"%{location.strip()}%"))
    if remote_only:
        stmt = stmt.where(Job.remote.is_(True))
    if source:
        stmt = stmt.where(Job.source == source)
    stmt = stmt.order_by(Job.published_at.desc().nullslast(), Job.id.desc())
    stmt = stmt.limit(limit).offset(offset)
    with SessionLocal() as session:
        return list(session.scalars(stmt))


@router.post("/import", response_model=ImportResponse)
async def import_jobs(payload: ImportRequest):
    try:
        jobs = await fetch_jobs(payload.source, payload.query.strip())
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Fonte de vagas temporariamente indisponível.") from exc

    inserted = 0
    updated = 0
    try:
        with SessionLocal.begin() as session:
            for job in jobs:
                values = {
                    "source": job.source,
                    "source_id": job.source_id,
                    "title": job.title,
                    "company": job.company,
                    "source_url": str(job.source_url),
                    "description": job.description,
                    "location": job.location,
                    "remote": job.remote,
                    "tags": job.tags,
                    "published_at": job.published_at,
                }
                stmt = insert(Job).values(**values)
                stmt = stmt.on_conflict_do_update(
                    constraint="uq_jobs_source_id",
                    set_={key: value for key, value in values.items() if key not in ("source", "source_id")},
                ).returning(literal_column("xmax") == 0)
                is_insert = session.scalar(stmt)
                if is_insert:
                    inserted += 1
                else:
                    updated += 1
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível.") from exc
    return ImportResponse(source=payload.source, fetched=len(jobs), inserted=inserted, updated=updated)
