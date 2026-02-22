from pydantic import BaseModel
from typing import Optional

class PartTimeJobCreate(BaseModel):
    title: str
    company_id: int
    location: Optional[str] = None
    salary: Optional[str] = None
    skills: Optional[str] = None
    description: Optional[str] = None

from app.schemas.company import CompanyResponse

class PartTimeJobResponse(BaseModel):
    id: int
    title: str
    company_id: int
    location: Optional[str] = None
    salary: Optional[str] = None
    skills: Optional[str] = None
    description: Optional[str] = None
    company: Optional[CompanyResponse] = None

    class Config:
        from_attributes = True

