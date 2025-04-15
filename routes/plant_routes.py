
# routes/plant_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta, date
import uuid
from typing import List

from models.database import SessionLocal
from models.plant import Plant
from models.photo import Photo
from models.recommendation import Recommendation
from models.response_models import PlantOut
from models.input_models import PlantCreate
from services.storage import upload_to_s3
from services.weather import get_weather_data
from services.gemini import (
    get_photo_prompt,
    call_gemini_api,
    parse_gemini_json_response
)
from utils.validators import get_plant_or_404


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", summary="List all plants", response_model=List[PlantOut])
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()

@router.post("/", summary="Add a new plant", response_model=PlantOut, tags=["Plants"])
def add_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    allowed_types = ["aloe", "cactus", "ficus", "sansevieria", "money tree"]
    if payload.type.lower() not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid plant type.")

    plant = Plant(
        id=uuid.uuid4(),
        name=payload.name,
        type=payload.type.lower(),
        last_watered=payload.last_watered,
        next_watering=None  # устанавливается позже через Gemini
    )
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant

@router.post(
    "/{plant_id}/water",
    summary="Mark the plant as watered and auto-update next watering",
    tags=["Plants"]
)
def mark_plant_watered(plant_id: UUID, db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    now = datetime.utcnow()

    # Обновляем дату последнего полива
    plant.last_watered = now
    plant.next_watering = None  # будет обновлено ниже

    # Получаем текущее фото
    photo = db.query(Photo).filter(Photo.plant_id == plant_id, Photo.is_current == True).first()
    if not photo:
        db.commit()
        return {
            "message": f"🌊 Plant '{plant.name}' watered, but no photo found.",
            "last_watered": now.isoformat()
        }

    # Определяем прошлый интервал полива
    interval = None
    if plant.last_watered and plant.next_watering:
        interval = (plant.next_watering - plant.last_watered).days

    # Генерация рекомендаций через Gemini
    prompt = get_photo_prompt(plant.name, previous_interval=interval)
    raw_response = call_gemini_api(prompt)
    parsed = parse_gemini_json_response(raw_response)

    recommendation_text = parsed.get("recommendation", raw_response)
    days = parsed.get("next_watering_in_days", 3)

    # Сохраняем рекомендацию
    rec = Recommendation(
        id=uuid.uuid4(),
        plant_id=plant_id,
        type="photo",
        content=recommendation_text
    )
    db.add(rec)

    # Обновляем следующую дату полива
    plant.next_watering = now + timedelta(days=days)

    db.commit()
    return {
        "message": f"🌊 Plant '{plant.name}' watered and re-analyzed!",
        "last_watered": now.isoformat(),
        "next_watering": plant.next_watering.isoformat(),
        "recommendation": recommendation_text
    }


@router.get(
    "/watering-today",
    summary="Get plants that need watering today",
    response_model=List[PlantOut],
    tags=["Notifications"]
)
def get_plants_to_water_today(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(Plant).filter(
        Plant.next_watering != None,
        Plant.next_watering <= today
    ).all()
