from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.db.dependencies import get_db, get_current_user
from fastapi.responses import StreamingResponse
from app.utils.resume_generator import generate_resume_pdf
from app.models.job_seeker_profile import JobSeekerProfile
from app.core.security import get_password_hash, verify_password, create_access_token
import io

router = APIRouter(prefix="/users", tags=["Users"])






@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()



@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=get_password_hash(user.password),  
        role=user.role,
        status="approved" # Auto-approve for immediate access
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


from app.schemas.user import UserLogin
from app.models.company import Company

@router.post("/login")
def login_user(user_creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_creds.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user_creds.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(subject=user.id)

    # Build user dict
    user_data = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "profile_image": user.profile_image if hasattr(user, 'profile_image') else None,
        "company": None
    }

    # If employer, also load their company
    if user.role == "employer":
        company = db.query(Company).filter(Company.user_id == user.id).first()
        if company:
            user_data["company"] = {
                "id": company.id,
                "company_name": company.company_name,
                "email": company.email,
                "phone": company.phone,
                "location": company.location,
                "website": company.website,
                "description": company.description,
                "industry": company.industry,
                "logo_url": company.logo_url,
            }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Example protected route to get current user info"""
    return current_user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.full_name:
        user.full_name = data.full_name
    if data.password:
        user.password = data.password
    if data.role:
        user.role = data.role
    if data.status:
        user.status = data.status
    if data.profile_image:
        user.profile_image = data.profile_image

    db.commit()
    db.refresh(user)
    return user


from app.schemas.user import AccountDelete

@router.delete("/{user_id}")
def delete_user(user_id: int, data: AccountDelete, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify Password
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password. Deletion aborted.")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/{user_id}/resume")
def download_resume(
    user_id: int, 
    template: str = "professional",
    show_salary: bool = True,
    show_location: bool = True,
    show_department: bool = True,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    profile = db.query(JobSeekerProfile).filter(JobSeekerProfile.user_id == user.id).first()
    if not profile:
        profile = JobSeekerProfile(user_id=user.id) 

    options = {
        "template": template,
        "show_salary": show_salary,
        "show_location": show_location,
        "show_department": show_department
    }

    pdf_bytes = generate_resume_pdf(user, profile, options)
    
    return StreamingResponse(
        io.BytesIO(bytes(pdf_bytes)), 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=resume_{user.full_name.replace(' ', '_')}.pdf"}
    )