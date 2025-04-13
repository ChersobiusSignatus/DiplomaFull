#routes/photo_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.photo import Photo
from models.plant import Plant
from services.storage import upload_to_s3
from uuid import UUID
import uuid
from response_models import PhotoOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{plant_id}/photos", summary="Upload a photo and mark it as current", response_model=PhotoOut)
def upload_photo(plant_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    s3_url = upload_to_s3(file)

    db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).update({"is_current": False})

    photo = Photo(id=uuid.uuid4(), plant_id=plant_id, s3_url=s3_url, is_current=True)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo



