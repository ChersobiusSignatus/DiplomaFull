
#models/schemas.py

from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime



class PlantCreate(BaseModel):
    name: str
    type: str

class SensorDataIn(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    pressure: Optional[float] = None
    gas_quality: Optional[float] = None


class GeoLocation(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
