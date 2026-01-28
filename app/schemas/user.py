from pydantic import BaseModel

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
    status: str | None = None


from app.schemas.companies import CompanyResponse

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    status: str
    company: CompanyResponse | None = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str
