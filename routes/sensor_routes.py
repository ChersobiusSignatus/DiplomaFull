### routes/sensor_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.plant import Plant
from models.sensor_data import SensorData
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{plant_id}/sensor-data", summary="Upload real-time sensor data")
def upload_sensor_data(
    plant_id: str,
    temperature: float,
    humidity: float,
    soil_moisture: float,
    light: float,
    pressure: float = None,
    gas_quality: float = None,
    db: Session = Depends(get_db)
):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    data = SensorData(
        id=uuid.uuid4(),
        plant_id=plant_id,
        temperature=temperature,
        humidity=humidity,
        soil_moisture=soil_moisture,
        light=light,
        pressure=pressure,
        gas_quality=gas_quality
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data