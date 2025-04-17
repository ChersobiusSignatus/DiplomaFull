#routes/photo_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.photo import Photo
from models.plant import Plant
from services.storage import upload_to_s3
from uuid import UUID
import uuid
from models.response_models import PhotoOut
from typing import List, Optional


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post(
    "/{plant_id}/photos",
    summary="Upload a plant photo and mark it as current",
    response_model=PhotoOut,
    tags=["Photos"]
)
def upload_photo(
    plant_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 🔍 Проверка: существует ли растение
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    # ☁️ Загрузка фото на S3
    s3_url = upload_to_s3(file)

    # 🧼 Убираем старое текущее фото (если есть)
    db.query(Photo).filter(
        Photo.plant_id == plant_id,
        Photo.is_current == True
    ).update({"is_current": False})

    # 📸 Сохраняем новое фото как текущее
    photo = Photo(
        id=uuid.uuid4(),
        plant_id=plant_id,
        s3_url=s3_url,
        is_current=True
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo


@router.get("/{plant_id}/photos")
def get_plant_photos(plant_id: UUID, db: Session = Depends(get_db)):
    photos = db.query(Photo).filter(Photo.plant_id == plant_id).all()
    return photos


@router.get("/photos/latest", summary="Get current photos for all plants", tags=["Photos"])
def get_latest_photos(db: Session = Depends(get_db)):
    # Получить только по одному текущему фото для каждого растения
    subquery = (
        db.query(Photo.plant_id, Photo.created_at)
        .filter(Photo.is_current == True)
        .distinct(Photo.plant_id)
        .subquery()
    )

    # Присоединить обратно к таблице Photo, чтобы получить остальные поля
    current_photos = (
        db.query(Photo)
        .join(subquery, (Photo.plant_id == subquery.c.plant_id) & (Photo.created_at == subquery.c.created_at))
        .all()
    )

    return [
        {
            "plant_id": str(photo.plant_id),
            "photo_url": photo.s3_url,
            "created_at": photo.created_at.isoformat()
        }
        for photo in current_photos
    ]

