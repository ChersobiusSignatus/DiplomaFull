# utils/validators.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.plant import Plant
from uuid import UUID

def get_plant_or_404(plant_id: UUID, db: Session) -> Plant:
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
