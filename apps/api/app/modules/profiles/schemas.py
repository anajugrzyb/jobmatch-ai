from pydantic import BaseModel, ConfigDict, Field


class ProfileInput(BaseModel):
    full_name: str = Field(default="", max_length=160)
    headline: str = Field(default="", max_length=240)
    location: str = Field(default="", max_length=160)
    email: str = Field(default="", max_length=254)
    skills: str = Field(default="", max_length=10000)
    experience: str = Field(default="", max_length=30000)
    education: str = Field(default="", max_length=10000)


class ProfileResponse(ProfileInput):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ResumeExtraction(BaseModel):
    text: str
    pages: int
    truncated: bool
