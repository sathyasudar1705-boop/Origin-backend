from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class PartTimeJob(Base):
    __tablename__ = "part_time_jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    location = Column(String(100))
    salary = Column(String(50))
    skills = Column(String(200))
    description = Column(Text)

    company = relationship("Company", back_populates="part_time_jobs")
