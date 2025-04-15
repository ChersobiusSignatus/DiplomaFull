#routes/diagnosis_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from uuid import UUID
from typing import List, Optional

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
    call_gemini_api,
    parse_gemini_json_response
)
from services.weather import get_weather_data

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
