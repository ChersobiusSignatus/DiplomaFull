# routes/diagnosis_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import List, Optional
import requests

from models.database import SessionLocal
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation
from models.response_models import RecommendationOut
from models.input_models import GeoLocation
from utils.validators import get_plant_or_404
from services.gemini import (
    get_photo_prompt,
    get_combined_prompt,
    call_gemini_api_with_image,
    parse_gemini_json_response
)
from services.weather import get_weather_data

router = APIRouter()

# ✅ Получение сессии БД через Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📸 Диагностика по фотографии
@router.post("/photo/{plant_id}", response_model=RecommendationOut)
def diagnose_by_photo(
    plant_id: UUID,
    db: Session = Depends(get_db),
):
    plant = get_plant_or_404(plant_id, db)
    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()

    if not photo:
        raise HTTPException(status_code=404, detail="No current photo found for diagnosis")

    last_recommendation = db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id
    ).order_by(Recommendation.created_at.desc()).first()

    previous_interval = None
    if last_recommendation and last_recommendation.next_watering and last_recommendation.last_watered:
        delta = (last_recommendation.next_watering - last_recommendation.last_watered).days
        previous_interval = max(delta, 1)

    prompt = get_photo_prompt(
        plant_name=plant.name,
        plant_type=plant.type,
        previous_interval=previous_interval,
        last_watered=plant.last_watered
    )

    try:
        image_response = requests.get(photo.s3_url)
        image_response.raise_for_status()
        image_bytes = image_response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download photo from S3: {e}")

    raw_response = call_gemini_api_with_image(image_bytes, prompt)
    parsed = parse_gemini_json_response(raw_response)

    recommendation = Recommendation(
        plant_id=plant_id,
        photo_id=photo.id,
        type="photo",
        content=parsed["recommendation"],
        last_watered=plant.last_watered,
        next_watering=parsed.get("next_watering_date"),
        created_at=datetime.utcnow()
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation

# 🔄 Комбинированная диагностика: фото + сенсоры + (опц.) погода
@router.post("/combined/{plant_id}", response_model=RecommendationOut)
def diagnose_combined(
    plant_id: UUID,
    location: Optional[GeoLocation] = None,
    db: Session = Depends(get_db),
):
    plant = get_plant_or_404(plant_id, db)

    photo = db.query(Photo).filter(
        Photo.plant_id == plant_id,
        Photo.is_current == True
    ).first()

    sensor = db.query(SensorData).filter(
        SensorData.plant_id == plant_id
    ).order_by(SensorData.created_at.desc()).first()

    if not photo or not sensor:
        raise HTTPException(status_code=404, detail="Photo or sensor data is missing")

    if location:
        weather = get_weather_data(location.latitude, location.longitude)
    else:
        weather = None

    last_recommendation = db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id
    ).order_by(Recommendation.created_at.desc()).first()

    previous_interval = None
    if last_recommendation and last_recommendation.next_watering and last_recommendation.last_watered:
        delta = (last_recommendation.next_watering - last_recommendation.last_watered).days
        previous_interval = max(delta, 1)

    prompt = get_combined_prompt(
        plant_name=plant.name,
        plant_type=plant.type,
        sensors=sensor,
        weather=weather,
        previous_interval=previous_interval,
        last_watered=plant.last_watered
    )

    try:
        image_response = requests.get(photo.s3_url)
        image_response.raise_for_status()
        image_bytes = image_response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download photo from S3: {e}")

    raw_response = call_gemini_api_with_image(image_bytes, prompt)
    parsed = parse_gemini_json_response(raw_response)

    recommendation = Recommendation(
        plant_id=plant_id,
        photo_id=photo.id,
        sensor_id=sensor.id,
        type="combined",
        content=parsed["recommendation"],
        last_watered=plant.last_watered,
        next_watering=parsed.get("next_watering_date"),
        created_at=datetime.utcnow()
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation

# 📜 Получить историю рекомендаций
@router.get("/recommendations/{plant_id}", response_model=List[RecommendationOut])
def get_recommendations(plant_id: UUID, db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    return db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id
    ).order_by(Recommendation.created_at.desc()).all()
