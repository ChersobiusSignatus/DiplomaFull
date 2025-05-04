

# routes/history_routes.py

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from uuid import UUID
from datetime import date
import requests

from models.database import get_db
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation

router = APIRouter()

@router.get("/plants/{plant_id}/history/{selected_date}")
def get_plant_history_by_date(plant_id: UUID, selected_date: date, db: Session = Depends(get_db)):
    # Рекомендация за этот день
    recommendation = db.query(Recommendation)\
        .filter(
            Recommendation.plant_id == plant_id,
            func.date(Recommendation.created_at) == selected_date
        ).order_by(Recommendation.created_at.desc()).first()

    # Сенсорные данные за этот день
    sensor = db.query(SensorData)\
        .filter(
            SensorData.plant_id == plant_id,
            func.date(SensorData.created_at) == selected_date
        ).order_by(SensorData.created_at.desc()).first()

    # Фото — последнее до или в этот день (не обязательно)
    photo = db.query(Photo)\
        .filter(
            Photo.plant_id == plant_id,
            func.date(Photo.created_at) <= selected_date
        ).order_by(Photo.created_at.desc()).first()

    if not recommendation and not sensor:
        raise HTTPException(status_code=404, detail="No data found for this date")

    alt_message = ""
    if not recommendation:
        prev_rec = db.query(func.max(func.date(Recommendation.created_at)))\
            .filter(
                Recommendation.plant_id == plant_id,
                func.date(Recommendation.created_at) < selected_date
            ).scalar()
        next_rec = db.query(func.min(func.date(Recommendation.created_at)))\
            .filter(
                Recommendation.plant_id == plant_id,
                func.date(Recommendation.created_at) > selected_date
            ).scalar()
        prev_str = prev_rec.isoformat() if prev_rec else "—"
        next_str = next_rec.isoformat() if next_rec else "—"
        alt_message = f"В этот день рекомендации не было. Попробуйте {prev_str} или {next_str}"

    image_bytes = None
    if photo and photo.s3_url:
        try:
            image_response = requests.get(photo.s3_url)
            image_response.raise_for_status()
            image_bytes = image_response.content
        except Exception:
            image_bytes = None

    return Response(
        content=image_bytes or b"No image available",
        media_type="image/jpeg" if image_bytes else "text/plain",
        headers={
            "X-Recommendation": recommendation.content if recommendation else alt_message,
            "X-Next-Watering": str(recommendation.next_watering) if recommendation else "",
            "X-Sensor-Temperature": str(sensor.temperature) if sensor else "",
            "X-Sensor-Humidity": str(sensor.humidity) if sensor else "",
            "X-Sensor-Light": str(sensor.light) if sensor else "",
            "X-Sensor-Soil": str(sensor.soil_moisture) if sensor else "",
            "X-Sensor-Gas": str(sensor.gas_quality) if sensor else ""
        }
    )
