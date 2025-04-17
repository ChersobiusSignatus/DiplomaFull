#routes/plant_details.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from models.database import get_db
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation
import requests
import base64

router = APIRouter()

@router.get("/{plant_id}/details")
def get_plant_details(plant_id: UUID, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    photo = (
        db.query(Photo)
        .filter(Photo.plant_id == plant_id)
        .order_by(Photo.created_at.desc())
        .first()
    )

    # 🔄 Конвертация фото по ссылке в base64
    photo_base64 = None
    if photo:
        try:
            response = requests.get(photo.s3_url)
            if response.status_code == 200:
                photo_base64 = base64.b64encode(response.content).decode('utf-8')
        except Exception:
            photo_base64 = None

    sensor = (
        db.query(SensorData)
        .filter(SensorData.plant_id == plant_id)
        .order_by(SensorData.created_at.desc())
        .first()
    )

    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.plant_id == plant_id)
        .order_by(Recommendation.created_at.desc())
        .first()
    )

    return {
        "plant_id": str(plant.id),
        "name": plant.name,
        "type": plant.type,
        "last_watered": plant.last_watered,
        "next_watering": plant.next_watering,
        "last_photo_base64": photo_base64,
        "last_sensor_data": {
            "temperature": sensor.temperature,
            "humidity": sensor.humidity,
            "soil_moisture": sensor.soil_moisture,
            "light": sensor.light,
            "gas_quality": sensor.gas_quality,
            "created_at": sensor.created_at,
        } if sensor else {
            "temperature": None,
            "humidity": None,
            "soil_moisture": None,
            "light": None,
            "gas_quality": None,
            "created_at": None,
        },
        "last_gemini_recommendation": {
            "text": recommendation.text,
            "created_at": recommendation.created_at,
        } if recommendation else {
            "text": None,
            "created_at": None,
        }
    }
