from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # job seeker / employer
    is_active = Column(Boolean, default=True)
    status = Column(String, default="pending") # pending / approved / rejected
    profile_image = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")
    company = relationship("Company", back_populates="owner", uselist=False, foreign_keys="Company.user_id", lazy="joined", cascade="all, delete-orphan")
    job_seeker_profile = relationship("JobSeekerProfile",back_populates="user",uselist=False,cascade="all, delete", lazy="joined")