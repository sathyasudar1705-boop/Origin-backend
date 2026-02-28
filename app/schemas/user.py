from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    profile_image: str | None = None
    status: str | None = None


from app.schemas.company import CompanyResponse

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    status: str
    profile_image: str | None = None
    company: CompanyResponse | None = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class AccountDelete(BaseModel):
    password: str
