# routes/history_routes.py

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime
import requests

from models.database import get_db
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation

router = APIRouter()

@router.get("/{plant_id}/history/{selected_date}")
def get_plant_history_by_date(plant_id: UUID, selected_date: str, db: Session = Depends(get_db)):
    try:
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Ищем по дате без учёта времени
    recommendation = db.query(Recommendation)\
        .filter(
            Recommendation.plant_id == plant_id,
            func.date(Recommendation.created_at) == parsed_date
        ).order_by(Recommendation.created_at.desc()).first()

    sensor = db.query(SensorData)\
        .filter(
            SensorData.plant_id == plant_id,
            func.date(SensorData.created_at) == parsed_date
        ).order_by(SensorData.created_at.desc()).first()

    photo = db.query(Photo)\
        .filter(
            Photo.plant_id == plant_id,
            func.date(Photo.created_at) <= parsed_date
        ).order_by(Photo.created_at.desc()).first()
    
    print("✅ Parsed date:", parsed_date)
    print("🧠 Recommendation match:", recommendation)
    print("📡 Sensor match:", sensor)

    if not recommendation and not sensor:
        raise HTTPException(status_code=404, detail="No data found for this date")

    alt_message = ""
    if not recommendation:
        prev = db.query(func.date(Recommendation.created_at))\
            .filter(Recommendation.plant_id == plant_id, Recommendation.created_at < parsed_date)\
            .order_by(Recommendation.created_at.desc()).first()
        next = db.query(func.date(Recommendation.created_at))\
            .filter(Recommendation.plant_id == plant_id, Recommendation.created_at > parsed_date)\
            .order_by(Recommendation.created_at.asc()).first()
        alt_message = f"Нет рекомендации. Попробуйте {prev[0]} или {next[0]}" if prev or next else "Нет рекомендации на эту дату"

    image_bytes = None
    if photo and photo.s3_url:
        try:
            image_response = requests.get(photo.s3_url)
            image_response.raise_for_status()
            image_bytes = image_response.content
        except:
            pass

    return Response(
        content=image_bytes or b"No image available",
        media_type="image/jpeg" if image_bytes else "text/plain",
        headers={
            "X-Recommendation": recommendation.content if recommendation else alt_message,
            "X-Next-Watering": str(recommendation.next_watering) if recommendation and recommendation.next_watering else "",
            "X-Sensor-Temperature": str(sensor.temperature) if sensor else "",
            "X-Sensor-Humidity": str(sensor.humidity) if sensor else "",
            "X-Sensor-Light": str(sensor.light) if sensor else "",
            "X-Sensor-Soil": str(sensor.soil_moisture) if sensor else "",
            "X-Sensor-Gas": str(sensor.gas_quality) if sensor else ""
        }
    )
