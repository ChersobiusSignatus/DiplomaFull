#models/response_models.py

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class PlantOut(BaseModel):
    id: UUID
    name: str
    type: str
    created_at: datetime

    class Config:
        orm_mode = True

class PhotoOut(BaseModel):
    id: UUID
    plant_id: UUID
    s3_url: str
    is_current: bool
    created_at: datetime

    class Config:
        orm_mode = True

class SensorDataOut(BaseModel):
    id: UUID
    plant_id: UUID
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    pressure: Optional[float] = None
    gas_quality: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True

class RecommendationOut(BaseModel):
    id: UUID
    plant_id: UUID
    type: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

