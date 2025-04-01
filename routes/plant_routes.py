from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.plant import Plant
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", summary="List all available plants")
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()

@router.post("/", summary="Add a new plant")
def add_plant(name: str, db: Session = Depends(get_db)):
    plant = Plant(id=uuid.uuid4(), name=name)
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant