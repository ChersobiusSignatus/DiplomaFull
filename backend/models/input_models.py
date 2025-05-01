# models/input_models.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ✅ Модель для создания нового растения
class PlantCreate(BaseModel):
    name: str = Field(example="My Aloe Vera")
    type: str = Field(example="aloe")  # Выбор из допустимых значений (валидация в route)
    last_watered: Optional[datetime] = None  # Опционально: дата последнего полива


# ✅ Входные данные с сенсоров (POST /sensor-data)
class SensorDataIn(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    gas_quality: Optional[float] = None


# ✅ Геолокация для прогноза погоды (diagnose_combined)
class GeoLocation(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
