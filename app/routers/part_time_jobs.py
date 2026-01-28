from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.part_time_jobs import PartTimeJob
from app.models.companies import Company
from app.schemas.part_time_jobs import PartTimeJobCreate, PartTimeJobResponse

router = APIRouter(
    prefix="/part_time_jobs",
    tags=["Part-Time Jobs"]
)


@router.post("/", response_model=PartTimeJobResponse)
def create_part_time_job(job: PartTimeJobCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == job.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    new_job = PartTimeJob(
        title=job.title,
        company_id=job.company_id,
        location=job.location,
        salary=job.salary,
        skills=job.skills,
        description=job.description
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return PartTimeJobResponse(
        id=new_job.id,
        title=new_job.title,
        company_id=new_job.company_id,
        company_name=company.company_name,
        location=new_job.location,
        salary=new_job.salary,
        skills=new_job.skills,
        description=new_job.description
    )


@router.get("/{job_id}", response_model=PartTimeJobResponse)
def get_part_time_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PartTimeJob).filter(PartTimeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    company = db.query(Company).filter(Company.id == job.company_id).first()

    return PartTimeJobResponse(
        id=job.id,
        title=job.title,
        company_id=job.company_id,
        company_name=company.company_name if company else "Unknown",
        location=job.location,
        salary=job.salary,
        skills=job.skills,
        description=job.description
    )


@router.get("/", response_model=list[PartTimeJobResponse])
def get_all_part_time_jobs(q: str = None, location: str = None, db: Session = Depends(get_db)):
    query = db.query(PartTimeJob)
    if q:
        query = query.filter(PartTimeJob.title.ilike(f"%{q}%") | PartTimeJob.description.ilike(f"%{q}%"))
    if location:
        query = query.filter(PartTimeJob.location.ilike(f"%{location}%"))
    
    jobs = query.all()
    response = []
    for job in jobs:
        company = db.query(Company).filter(Company.id == job.company_id).first()
        response.append(
            PartTimeJobResponse(
                id=job.id, # Added in previous step
                title=job.title,
                company_id=job.company_id,
                company_name=company.company_name if company else "Unknown",
                location=job.location,
                salary=job.salary,
                skills=job.skills,
                description=job.description
            )
        )
    return response



@router.put("/{job_id}", response_model=PartTimeJobResponse)
def update_part_time_job(job_id: int, job_update: PartTimeJobCreate, db: Session = Depends(get_db)):
    job = db.query(PartTimeJob).filter(PartTimeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    company = db.query(Company).filter(Company.id == job_update.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    job.title = job_update.title
    job.company_id = job_update.company_id
    job.location = job_update.location
    job.salary = job_update.salary
    job.skills = job_update.skills
    job.description = job_update.description

    db.commit()
    db.refresh(job)

    return PartTimeJobResponse(
        id=job.id,
        title=job.title,
        company_id=job.company_id,
        company_name=company.company_name,
        location=job.location,
        salary=job.salary,
        skills=job.skills,
        description=job.description
    )



@router.delete("/{job_id}")
def delete_part_time_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PartTimeJob).filter(PartTimeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": f"Part-time job with id {job_id} deleted successfully."}
