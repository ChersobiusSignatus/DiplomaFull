# utils/validators.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from models.plant import Plant
from models.recommendation import Recommendation
from datetime import date

def get_plant_or_404(plant_id: UUID, db: Session) -> Plant:
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

def check_daily_limit(plant_id: UUID, db: Session, limit: int = 20):
    today = date.today()
    count = db.query(Recommendation).filter(
        Recommendation.plant_id == plant_id,
        Recommendation.created_at >= today
    ).count()
    if count >= limit:
        raise HTTPException(status_code=429, detail="Daily limit of 20 diagnoses reached.")

