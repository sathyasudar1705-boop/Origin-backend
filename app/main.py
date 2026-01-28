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
    allow_origins=["*"],
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