from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from sqlalchemy import text
from app.models.job_seeker_profile import JobSeekerProfile
from app.db.dependencies import get_db
from app.schemas.job_seeker_profile import JobSeekerProfileCreate,JobSeekerProfileUpdate,JobSeekerProfileResponse,JobSeekerProfileView

router = APIRouter(prefix="/jobseeker-profile", tags=["Job Seeker Profile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.get("/{user_id}", response_model=JobSeekerProfileView)
def get_profile(user_id: int, db: Session = Depends(get_db)):

    query = text("""
        SELECT
            u.full_name AS name,
            u.email,
            jsp.location,
            jsp.phone,
            jsp.gender,
            jsp.dob,
            jsp.address,
            jsp.education,
            jsp.skills,
            jsp.desired_job,
            jsp.department,
            jsp.preferred_work_location,
            jsp.expected_salary,
            jsp.resume_url
        FROM users u
        JOIN job_seeker_profiles jsp ON u.id = jsp.user_id
        WHERE u.id = :user_id
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Job seeker profile not found")

    return result
  


@router.post("/", response_model=JobSeekerProfileResponse)
def create_profile(data: JobSeekerProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(JobSeekerProfile).filter(
        JobSeekerProfile.user_id == data.user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = JobSeekerProfile(**data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/user/{user_id}", response_model=JobSeekerProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(JobSeekerProfile).filter(
        JobSeekerProfile.user_id == user_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/{profile_id}", response_model=JobSeekerProfileResponse)
def update_profile(profile_id: int, data: JobSeekerProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(JobSeekerProfile).get(profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile



@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(JobSeekerProfile).get(profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}
