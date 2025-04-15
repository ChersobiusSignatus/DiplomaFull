# models/sensor_data.py

from datetime import datetime
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)

    temperature = Column(Float)         # Температура воздуха (°C)
    humidity = Column(Float)            # Влажность воздуха (%)
    soil_moisture = Column(Float)       # Влажность почвы (аналоговое значение)
    light = Column(Float)               # Освещённость (lux)    
    gas_quality = Column(Float)         # Качество воздуха (MQ-9), если доступно

    created_at = Column(DateTime, default=datetime.utcnow)
