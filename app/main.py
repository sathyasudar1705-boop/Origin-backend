from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import user
from app.routers import job_seeker_profile
# from app.routers import employer_profile
from app.routers import jobs
from app.routers import job_application
from app.routers import companies
from app.routers import part_time_jobs


Base.metadata.create_all(bind=engine)

app = FastAPI(title="OriginX - Users API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://origin-frontend-sepia.vercel.app",
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "*"  # Allow all origins (can remove this for stricter security)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(job_seeker_profile.router)
# app.include_router(employer_profile.router)
app.include_router(jobs.router)
app.include_router(job_application.router)
app.include_router(companies.router)
app.include_router(part_time_jobs.router)

from fastapi.staticfiles import StaticFiles
import os

# Create uploads directory if getting started
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Stats endpoint for landing page
from app.db.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.user import User
from app.models.job import Job
from app.models.part_time_job import PartTimeJob
from app.models.company import Company
from app.models.job_application import JobApplication

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get platform statistics for landing page"""
    users_count = db.query(User).count()
    jobs_count = db.query(Job).count() + db.query(PartTimeJob).count()
    companies_count = db.query(Company).count()
    applications_count = db.query(JobApplication).count()
    
    return {
        "users": users_count,
        "jobs": jobs_count,
        "companies": companies_count,
        "applications": applications_count
    }
