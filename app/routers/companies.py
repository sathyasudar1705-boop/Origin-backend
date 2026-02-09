from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import text
import shutil
import os
from pathlib import Path
from app.db.dependencies import get_db
from app.models.companies import Company
from app.models.user import User
from app.schemas.companies import CompanyCreate, CompanyUpdate, CompanyResponse, CompanyRegister

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)





@router.post("/")
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    new_company = Company(**company.dict())

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

@router.post("/register")
def register_company(data: CompanyRegister, db: Session = Depends(get_db)):
    # 1. Create User
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        full_name=data.full_name,
        email=data.email,
        password=data.password,
        role="employer",
        status="approved" # Employers are auto-approved for now
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 2. Create Company linked to user
    new_company = Company(
        company_name=data.company_name,
        email=data.email,
        location=data.location,
        user_id=new_user.id
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    # Refresh user to load the joined 'company' relationship
    db.refresh(new_user)

    # Return the user (who now has .company relationship via Company.user_id)
    return new_user


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company




@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company_data.dict(exclude_unset=True).items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)
    return company




@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.commit()
    return {"message": "Company deleted successfully"}


@router.post("/{company_id}/logo")
async def upload_company_logo(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Create uploads directory if not exists (backend/uploads)
    # Using relative path for simplicity, assuming running from backend root or similar
    UPLOAD_DIR = "uploads" 
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"company_{company_id}_{int(datetime.now().timestamp())}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update database with URL (served via static mount)
    # URL format: /uploads/filename
    logo_url = f"/uploads/{unique_filename}"
    
    company.logo_url = logo_url
    db.commit()
    db.refresh(company)

    return {"logo_url": logo_url}
