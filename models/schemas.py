
#models/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from uuid import UUID



class PlantCreate(BaseModel):
    name: str = Field(example="My Aloe Vera")
    type: str = Field(example="aloe")

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
