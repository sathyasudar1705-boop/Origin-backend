from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobApplicationCreate(BaseModel):
    job_id: Optional[int] = None
    pt_job_id: Optional[int] = None
    user_id: int
    full_name: str
    email: str
    phone: str
    resume_url: str
    experience: str
    skills: str
    expected_salary: str
    current_location: str

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None  

class JobApplicationResponse(BaseModel):
    id: int
    job_id: Optional[int] = None
    pt_job_id: Optional[int] = None
    user_id: Optional[int] = None
    status: str
    created_at: Optional[str] = None
    job_title: Optional[str] = None
    job_location: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    expected_salary: Optional[str] = None
    current_location: Optional[str] = None


    class Config:
        from_attributes = True
