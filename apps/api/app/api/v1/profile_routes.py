from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy import select

from app.db.session import SessionLocal
from app.modules.profiles.models import ProfessionalProfile
from app.modules.profiles.pdf import MAX_UPLOAD_BYTES, extract_pdf
from app.modules.profiles.schemas import ProfileInput, ProfileResponse, ResumeExtraction

router = APIRouter(prefix="/api/v1", tags=["professional-profile"])


@router.get("/profile", response_model=ProfileResponse | None)
def get_profile():
    with SessionLocal() as session:
        profile = session.scalar(select(ProfessionalProfile).where(ProfessionalProfile.id == 1))
        return profile


@router.put("/profile", response_model=ProfileResponse)
def save_profile(payload: ProfileInput):
    with SessionLocal.begin() as session:
        profile = session.get(ProfessionalProfile, 1)
        if profile is None:
            profile = ProfessionalProfile(id=1)
            session.add(profile)
        for key, value in payload.model_dump().items():
            setattr(profile, key, value.strip())
        session.flush()
        session.refresh(profile)
        result = ProfileResponse.model_validate(profile)
    return result


@router.post("/resume/extract", response_model=ResumeExtraction)
async def extract_resume(file: Annotated[UploadFile, File()]):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=415, detail="Envie um arquivo PDF.")
    try:
        data = await file.read(MAX_UPLOAD_BYTES + 1)
    finally:
        await file.close()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="O limite de upload é 5 MB.")
    text, pages, truncated = extract_pdf(data)
    return ResumeExtraction(text=text, pages=pages, truncated=truncated)
