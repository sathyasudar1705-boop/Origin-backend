from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    company_id: int
    title: str
    description: str
    skills_required: str
    location: str
    salary: str

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None

from app.schemas.companies import CompanyResponse

class JobResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None
    company: Optional[CompanyResponse] = None

    class Config:
        from_attributes = True
