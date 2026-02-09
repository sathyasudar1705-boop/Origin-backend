from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from datetime import date
from typing import Optional

class JobSeekerProfile(Base):
    __tablename__ = "job_seeker_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    dob: Mapped[Optional[date]] = mapped_column(Date)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(String)
    skills: Mapped[Optional[str]] = mapped_column(String)
    experience: Mapped[Optional[int]] = mapped_column()  
    education: Mapped[Optional[str]] = mapped_column(String)
    department: Mapped[Optional[str]] = mapped_column(String)
    desired_job: Mapped[Optional[str]] = mapped_column(String)
    preferred_work_location: Mapped[Optional[str]] = mapped_column(String)
    expected_salary: Mapped[Optional[str]] = mapped_column(String)
    resume_url: Mapped[Optional[str]] = mapped_column(String)
    location: Mapped[Optional[str]] = mapped_column(String)
    summary: Mapped[Optional[str]] = mapped_column(String)
    projects: Mapped[Optional[str]] = mapped_column(String)
    github_url: Mapped[Optional[str]] = mapped_column(String)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String)

    user: Mapped["User"] = relationship("User", back_populates="job_seeker_profile")
