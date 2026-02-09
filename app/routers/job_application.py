from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import SessionLocal
from app.models.job_application import JobApplication
from app.db.dependencies import get_db
from app.schemas.job_application import JobApplicationCreate,JobApplicationUpdate,JobApplicationResponse
from app.utils.email import send_application_alert

router = APIRouter(prefix="/applications", tags=["Job Applications"])



@router.post("/", response_model=JobApplicationResponse)
def create_application(data: JobApplicationCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if data.job_id:
        existing = db.query(JobApplication).filter(
            JobApplication.job_id == data.job_id,
            JobApplication.user_id == data.user_id
        ).first()
    elif data.pt_job_id:
        existing = db.query(JobApplication).filter(
            JobApplication.pt_job_id == data.pt_job_id,
            JobApplication.user_id == data.user_id
        ).first()
    else:
        existing = None

    if existing:
        # Instead of error, update the existing application
        app_data = data.dict(exclude_unset=True)
        app_data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        app_data["status"] = "Applied" # Reset status to Applied on re-apply
        
        for key, value in app_data.items():
            setattr(existing, key, value)
        
        db.commit()
        db.refresh(existing)
        
        # Trigger email notification
        try:
            if existing.job:
                background_tasks.add_task(send_application_alert, existing.job.company.email, existing.full_name, existing.job.title)
            elif existing.pt_job:
                background_tasks.add_task(send_application_alert, existing.pt_job.company.email, existing.full_name, existing.pt_job.title)
        except Exception as e:
            print(f"Error triggering email: {e}")

        return existing

    app_data = data.dict()
    app_data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    
    # Ensure mutually exclusive job IDs (though frontend should handle this)
    if app_data.get("job_id") and app_data.get("pt_job_id"):
        # For safety, if both are present (shouldn't happen), prefer regular job
        app_data["pt_job_id"] = None

    try:
        app_obj = JobApplication(**app_data)
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)

        # Trigger email notification
        try:
            if app_obj.job:
                background_tasks.add_task(send_application_alert, app_obj.job.company.email, app_obj.full_name, app_obj.job.title)
            elif app_obj.pt_job:
                background_tasks.add_task(send_application_alert, app_obj.pt_job.company.email, app_obj.full_name, app_obj.pt_job.title)
        except Exception as e:
            print(f"Error triggering email: {e}")

        return app_obj
    except Exception as e:
        db.rollback()
        print(f"Error creating application: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/", response_model=list[JobApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(JobApplication).all()

from app.models.jobs import Job
from app.models.part_time_jobs import PartTimeJob

@router.get("/user/{user_id}", response_model=list[JobApplicationResponse])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    apps = db.query(JobApplication).filter(JobApplication.user_id == user_id).all()
    for app in apps:
        if app.job:
            app.job_title = app.job.title
            app.job_location = app.job.location
        elif app.pt_job:
            app.job_title = app.pt_job.title
            app.job_location = app.pt_job.location
    return apps

@router.get("/company/{company_id}", response_model=list[JobApplicationResponse])
def get_company_applications(company_id: int, db: Session = Depends(get_db)):
    # Applications for regular jobs
    full_time_apps = db.query(JobApplication).join(Job).filter(Job.company_id == company_id).all()
    # Applications for part-time jobs
    part_time_apps = db.query(JobApplication).join(PartTimeJob).filter(PartTimeJob.company_id == company_id).all()
    
    all_apps = full_time_apps + part_time_apps
    
    for app in all_apps:
        if app.job:
            app.job_title = app.job.title
            app.job_location = app.job.location
        elif app.pt_job:
            app.job_title = app.pt_job.title
            app.job_location = app.pt_job.location
            
    return all_apps


@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).get(application_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(application_id: int, data: JobApplicationUpdate, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).get(application_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(app_obj, key, value)

    db.commit()
    db.refresh(app_obj)
    return app_obj


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).get(application_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app_obj)
    db.commit()
    return {"message": "Application deleted successfully"}
