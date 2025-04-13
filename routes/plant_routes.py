### routes/plant_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.plant import Plant
import uuid
from typing import List
from response_models import PlantOut
from schemas import PlantCreate 
from response_models import PlantOut
from typing import List, Optional
from uuid import UUID


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", summary="List all available plants", response_model=List[PlantOut])
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()

@router.post(
    "/",
    summary="Add a new plant with type",
    response_model=PlantOut,
    tags=["Plants"]
)
def add_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    allowed_types = ["aloe", "cactus", "ficus", "sansevieria", "money tree"]
    if payload.type.lower() not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid plant type.")

    plant = Plant(id=uuid.uuid4(), name=payload.name, type=payload.type.lower())
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant
