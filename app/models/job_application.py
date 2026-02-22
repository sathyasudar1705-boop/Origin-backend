from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    pt_job_id = Column(Integer, ForeignKey("part_time_jobs.id"))
    user_id = Column(Integer, ForeignKey("users.id")) 
    status = Column(String, default="Applied")
    created_at = Column(String) 
    
    # Application details snapshot
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    resume_url = Column(String)
    experience = Column(String)
    skills = Column(String)
    expected_salary = Column(String)
    current_location = Column(String)
    
    job = relationship("Job", back_populates="applications")
    pt_job = relationship("PartTimeJob")
    user = relationship("User", back_populates="applications")