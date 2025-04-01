from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.photo import Photo
from models.plant import Plant
from services.storage import upload_to_s3
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{plant_id}/photos", summary="Upload a photo and mark it as current")
def upload_photo(plant_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate plant exists
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    # Upload file to S3
    s3_url = upload_to_s3(file)

    # Mark existing photos as not current
    db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).update({"is_current": False})

    # Add new photo
    photo = Photo(id=uuid.uuid4(), plant_id=plant_id, s3_url=s3_url, is_current=True)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo