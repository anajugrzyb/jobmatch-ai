from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    source: str
    source_url: str | None
    description: str | None
    location: str
    remote: bool
    tags: str
    published_at: datetime | None


class ImportRequest(BaseModel):
    source: str = Field(pattern="^(remotive|arbeitnow)$")
    query: str = Field(default="", max_length=100)


class ImportResponse(BaseModel):
    source: str
    fetched: int
    inserted: int
    updated: int


class NormalizedJob(BaseModel):
    source: str
    source_id: str
    title: str
    company: str
    source_url: HttpUrl
    description: str = ""
    location: str = ""
    remote: bool = False
    tags: str = ""
    published_at: datetime | None = None
