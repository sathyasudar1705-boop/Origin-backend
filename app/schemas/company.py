from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    company_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

class CompanyRegister(BaseModel):
    full_name: str
    email: str
    password: str
    company_name: str
    location: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None
    logo: Optional[str] = None
    is_verified: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    company_name: str
    email: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    logo: Optional[str] = None

    class Config:
        from_attributes = True
