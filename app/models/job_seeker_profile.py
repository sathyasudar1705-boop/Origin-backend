from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class JobSeekerProfile(Base):
    __tablename__ = "job_seeker_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    gender = Column(String(10))
    dob = Column(Date)
    phone = Column(String(20))
    address = Column(String)
    skills = Column(String)
    experience = Column(Integer)  
    education = Column(String)
    department = Column(String)
    desired_job = Column(String)
    preferred_work_location = Column(String)
    expected_salary = Column(String)
    resume_url = Column(String)
    location = Column(String)


    
    user = relationship("User", back_populates="job_seeker_profile")
