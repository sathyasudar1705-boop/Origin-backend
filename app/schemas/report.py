from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportCreate(BaseModel):
    reporter_id: int
    reported_user_id: int
    reason: str

class ReportUpdate(BaseModel):
    status: str

class ReportResponse(BaseModel):
    id: int
    reporter_id: int
    reported_user_id: int
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
