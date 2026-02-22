from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import user
from app.routers import job_seeker_profile
# from app.routers import employer_profile
from app.routers import jobs
from app.routers import job_application
from app.routers import companies
from app.routers import part_time_jobs
from app.routers import upload
from app.routers import news


import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    # Note: In serverless, this runs on cold starts.
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    yield
    # Shutdown: Clean up resources if needed
    logger.info("Shutting down...")

app = FastAPI(title="OriginX - Users API", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://origin-frontend-sepia.vercel.app",
        "https://origin-frontend-nine.vercel.app", # Potential production URL
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "*" 
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
app.include_router(upload.router)
app.include_router(news.router)



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

@app.get("/test-job", response_model=dict)
def test_job(db: Session = Depends(get_db)):
    """Example endpoint to return a Job instance (schema serialized)"""
    job = db.query(Job).first()
    if not job:
        return {"message": "No jobs found in database"}
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "status": job.status
    }
