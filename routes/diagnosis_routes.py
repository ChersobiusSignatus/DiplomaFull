#routes/diagnosis_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
import uuid
from typing import List, Optional

from response_models import RecommendationOut
from utils.validators import get_plant_or_404
from models.database import SessionLocal
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation
from services.gemini import get_photo_prompt, get_combined_prompt, call_gemini_api
from services.weather import get_weather_data
from response_models import RecommendationOut
from schemas import GeoLocation 




router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/photo/{plant_id}",
    summary="Diagnose based on the latest photo",
    response_model=RecommendationOut,
    tags=["Diagnosis"]
)
def diagnose_photo(
    plant_id: UUID = Path(description="Plant UUID"),
    db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()
    if not photo:
        raise HTTPException(status_code=404, detail="No current photo found")

    # daily limit check (max 20)
    from datetime import date
    today = date.today()
    count = db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id,
        Recommendation.created_at >= today
    ).count()
    if count >= 20:
        raise HTTPException(status_code=429, detail="Daily limit of 20 diagnoses reached.")

    prompt = get_photo_prompt(plant.name)
    response = call_gemini_api(prompt)

    rec = Recommendation(id=uuid.uuid4(), plant_id=plant_id, type="photo", content=response)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.post(
    "/combined/{plant_id}",
    summary="Diagnose using photo + sensors + weather",
    response_model=RecommendationOut,
    tags=["Diagnosis"]
)
def diagnose_combined(plant_id: UUID, location: GeoLocation, db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()
    sensors = db.query(SensorData).filter(SensorData.plant_id == plant_id).order_by(SensorData.created_at.desc()).first()

    if not photo or not sensors:
        raise HTTPException(status_code=404, detail="Missing photo or sensor data")

    # daily limit check (max 20)
    from datetime import date
    today = date.today()
    count = db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id,
        Recommendation.created_at >= today
    ).count()
    if count >= 20:
        raise HTTPException(status_code=429, detail="Daily limit of 20 diagnoses reached.")

    weather = None
    if location.latitude is not None and location.longitude is not None:
        weather = get_weather_data(location.latitude, location.longitude)

    prompt = get_combined_prompt(plant.name, sensors, weather)
    response = call_gemini_api(prompt)

    rec = Recommendation(id=uuid.uuid4(), plant_id=plant_id, type="combined", content=response)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.get(
    "/recommendations/{plant_id}",
    summary="Get AI-generated recommendations for a specific plant (latest 5, optional date filter)",
    response_model=List[RecommendationOut],
    tags=["Recommendations"]
)
def get_recommendations(
    plant_id: str,
    date_from: Optional[str] = None,
    db: Session = Depends(get_db)
):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    query = db.query(Recommendation).filter(Recommendation.plant_id == plant_id)

    if date_from:
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(Recommendation.created_at >= parsed_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    recs = query.order_by(Recommendation.created_at.desc()).limit(5).all()
    return recs
