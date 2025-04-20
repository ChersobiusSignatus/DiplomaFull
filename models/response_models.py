#models/response_models.py


from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# ✅ Используется для GET /plants/... (включает поля полива)
class PlantOut(BaseModel):
    id: UUID
    name: str
    type: str
    created_at: datetime
    last_watered: Optional[datetime]
    next_watering: Optional[datetime]

    class Config:
        from_attributes = True


# ✅ Используется после загрузки фото
class PhotoOut(BaseModel):
    id: UUID
    plant_id: UUID
    s3_url: str
    is_current: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ✅ Используется после загрузки сенсоров
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
        from_attributes = True


# ✅ Используется для ответа от Gemini
class RecommendationOut(BaseModel):
    id: UUID
    plant_id: UUID
    type: str                   # "photo" / "combined"
    content: str                # Текстовая рекомендация
    created_at: datetime

    class Config:
        from_attributes = True
