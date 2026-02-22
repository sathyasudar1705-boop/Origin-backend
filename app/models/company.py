from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    location = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    industry = Column(String(100))
    logo_url = Column(String(500), nullable=True)
    logo = Column(String(500), nullable=True) # Explicitly added as requested
    is_verified = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))


    
    owner = relationship("User", back_populates="company")
    part_time_jobs = relationship("PartTimeJob",back_populates="company",cascade="all, delete")
    jobs = relationship("Job",back_populates="company",cascade="all, delete")