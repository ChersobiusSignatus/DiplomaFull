#routes/plant_details.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from models.database import get_db
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation

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
    "next_watering": recommendation.next_watering,  
    "last_photo": photo.s3_url if photo else None,
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
        "recommendation": recommendation.content,
        "next_watering_date": recommendation.next_watering,
        "created_at": recommendation.created_at,
    } if recommendation else {
        "recommendation": None,
        "next_watering_date": None,
        "created_at": None,
    }
}





