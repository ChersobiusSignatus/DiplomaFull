from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation
from services.gemini import get_photo_prompt, get_combined_prompt, call_gemini_api
from services.weather import get_weather_data
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/photo/{plant_id}", summary="Diagnose based on the latest photo")
def diagnose_photo(plant_id: str, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()
    if not photo:
        raise HTTPException(status_code=404, detail="No current photo found")

    prompt = get_photo_prompt(plant.name)
    response = call_gemini_api(prompt)

    rec = Recommendation(id=uuid.uuid4(), plant_id=plant_id, type="photo", content=response)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.post("/combined/{plant_id}", summary="Diagnose using photo + sensors + weather")
def diagnose_combined(plant_id: str, latitude: float = None, longitude: float = None, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()
    sensors = db.query(SensorData).filter(SensorData.plant_id == plant_id).order_by(SensorData.created_at.desc()).first()

    if not photo or not sensors:
        raise HTTPException(status_code=404, detail="Missing photo or sensor data")

    weather = get_weather_data(latitude, longitude) if latitude and longitude else None

    prompt = get_combined_prompt(plant.name, sensors, weather)
    response = call_gemini_api(prompt)

    rec = Recommendation(id=uuid.uuid4(), plant_id=plant_id, type="combined", content=response)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec