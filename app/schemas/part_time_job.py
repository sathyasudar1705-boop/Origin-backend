from pydantic import BaseModel
from typing import Optional

class PartTimeJobCreate(BaseModel):
    title: str
    company_id: int
    location: Optional[str] = None
    salary: Optional[str] = None
    skills: Optional[str] = None
    description: Optional[str] = None

class PartTimeJobResponse(BaseModel):
    id: int
    title: str
    company_id: int
    company_name: str
    location: Optional[str] = None
    salary: Optional[str] = None
    skills: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
