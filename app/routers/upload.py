from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.company import Company
import cloudinary.uploader
import app.core.cloudinary_config # Ensure config is loaded
from typing import List

router = APIRouter(prefix="/api", tags=["Upload"])

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB

def validate_image(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    # Check size would require reading it, but for now we'll rely on UploadFile
    # A better way is to check content-length header if provided or read a chunk

@router.post("/users/upload-profile-image")
async def upload_user_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_image(file)
    
    # DEBUG: Check Cloudinary config values
    import cloudinary
    cfg = cloudinary.Config()
    print(f"DEBUG: Cloud Name: {cfg.cloud_name}")
    print(f"DEBUG: API Key: {cfg.api_key}")
    secret = cfg.api_secret or ""
    print(f"DEBUG: API Secret: {secret[:4]}...{secret[-4:] if len(secret) > 4 else ''}")
    
    try:
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="originx/users/profile_images",
            public_id=f"user_{current_user.id}"
        )
        image_url = upload_result.get("secure_url")
        
        current_user.profile_image = image_url
        db.commit()
        db.refresh(current_user)
        
        return {
            "message": "Upload successful",
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.post("/companies/upload-logo")
async def upload_company_logo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can upload company logos"
        )
    
    company = db.query(Company).filter(Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found"
        )
        
    validate_image(file)
    
    try:
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="originx/companies/profile_images",
            public_id=f"company_{company.id}"
        )
        image_url = upload_result.get("secure_url")
        
        company.logo = image_url
        company.logo_url = image_url # Keep both sync for now
        db.commit()
        db.refresh(company)
        
        return {
            "message": "Upload successful",
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )
