from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProfessionalProfile(Base):
    __tablename__ = "professional_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160), default="", nullable=False)
    headline: Mapped[str] = mapped_column(String(240), default="", nullable=False)
    location: Mapped[str] = mapped_column(String(160), default="", nullable=False)
    email: Mapped[str] = mapped_column(String(254), default="", nullable=False)
    skills: Mapped[str] = mapped_column(Text, default="", nullable=False)
    experience: Mapped[str] = mapped_column(Text, default="", nullable=False)
    education: Mapped[str] = mapped_column(Text, default="", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
