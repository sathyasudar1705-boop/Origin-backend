from pydantic import BaseModel
from typing import Optional
from datetime import date



class JobSeekerProfileCreate(BaseModel):
    user_id: int
    gender: Optional[str] = None
    dob: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[int] = None
    education: Optional[str] = None
    department: Optional[str] = None
    desired_job: Optional[str] = None
    preferred_work_location: Optional[str] = None
    expected_salary: Optional[str] = None
    location: Optional[str] = None
    resume_url: Optional[str] = None


class JobSeekerProfileUpdate(BaseModel):
    gender: Optional[str] = None
    dob: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    skills: Optional[str] = None
    experience: Optional[int] = None
    education: Optional[str] = None
    department: Optional[str] = None
    desired_job: Optional[str] = None
    preferred_work_location: Optional[str] = None
    expected_salary: Optional[str] = None

    location: Optional[str] = None
    resume_url: Optional[str] = None


class JobSeekerProfileResponse(BaseModel):
    id: int
    user_id: int

    gender: Optional[str]
    dob: Optional[date]
    phone: Optional[str]
    address: Optional[str]
    skills: Optional[str]
    experience: Optional[int]
    education: Optional[str]
    department: Optional[str]
    desired_job: Optional[str]
    preferred_work_location: Optional[str]
    expected_salary: Optional[str]
    location: Optional[str]
    resume_url: Optional[str]

    class Config:
        from_attributes = True




class JobSeekerProfileView(BaseModel):
    name: str
    email: str
    location: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    dob: Optional[date]
    address: Optional[str]
    education: Optional[str]
    skills: Optional[str]
    desired_job: Optional[str]
    department: Optional[str]
    preferred_work_location: Optional[str]
    expected_salary: Optional[str]
    resume_url: Optional[str]

    class Config:
        from_attributes = True