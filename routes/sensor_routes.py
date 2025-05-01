# routes/sensor_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import uuid

from models.database import SessionLocal
from models.sensor_data import SensorData
from models.plant import Plant
from models.response_models import SensorDataOut
from models.input_models import SensorDataIn
from utils.validators import get_plant_or_404


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/{plant_id}/sensor-data",
    summary="Upload real-time sensor data",
    response_model=SensorDataOut,
    tags=["Sensors"]
)
def upload_sensor_data(
    plant_id: UUID,
    payload: SensorDataIn,
    db: Session = Depends(get_db)
):
    plant = get_plant_or_404(plant_id, db)

    data = SensorData(
        id=uuid.uuid4(),
        plant_id=plant_id,
        temperature=payload.temperature,
        humidity=payload.humidity,
        soil_moisture=payload.soil_moisture,
        light=payload.light,
        gas_quality=payload.gas_quality
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
