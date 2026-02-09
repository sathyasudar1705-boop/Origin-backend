from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.dependencies import get_db
from app.models import report as models
from app.schemas import report as schemas

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.post("/", response_model=schemas.ReportResponse)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/", response_model=List[schemas.ReportResponse])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()

@router.put("/{report_id}", response_model=schemas.ReportResponse)
def update_report_status(report_id: int, status_update: schemas.ReportUpdate, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.status = status_update.status
    db.commit()
    db.refresh(report)
    return report
