from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String)
    skills_required = Column(String)
    location = Column(String)
    salary = Column(String)
    status = Column(String, default="pending") # pending / approved / rejected


    company = relationship("Company", back_populates="jobs")
    applications = relationship("JobApplication",back_populates="job",cascade="all, delete")
