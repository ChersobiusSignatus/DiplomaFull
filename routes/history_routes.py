# routes/history_routes.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
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
    # 1. Найти фото за выбранный день (или последнее до него)
    photo = db.query(Photo)\
        .filter(Photo.plant_id == plant_id, Photo.created_at <= selected_date)\
        .order_by(Photo.created_at.desc())\
        .first()

    # 2. Найти последнюю рекомендацию за выбранный день
    recommendation = db.query(Recommendation)\
        .filter(Recommendation.plant_id == plant_id, cast(Recommendation.created_at, Date) == selected_date)\
        .order_by(Recommendation.created_at.desc())\
        .first()

    # 3. Найти последнее показание сенсора за день
    sensor = db.query(SensorData)\
        .filter(SensorData.plant_id == plant_id, cast(SensorData.created_at, Date) == selected_date)\
        .order_by(SensorData.created_at.desc())\
        .first()

    if not photo and not recommendation and not sensor:
        raise HTTPException(status_code=404, detail="No data found for this date")

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
            "X-Recommendation": recommendation.recommendation if recommendation else "",
            "X-Next-Watering": str(recommendation.next_watering) if recommendation else "",
            "X-Sensor-Temperature": str(sensor.temperature) if sensor else "",
            "X-Sensor-Humidity": str(sensor.humidity) if sensor else "",
            "X-Sensor-Light": str(sensor.light) if sensor else "",
            "X-Sensor-Soil": str(sensor.soil_moisture) if sensor else "",
            "X-Sensor-Gas": str(sensor.gas_quality) if sensor else ""
        }
    )
