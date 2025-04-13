#models/sensor_data.py
import datetime
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional

import uuid
from .database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    soil_moisture = Column(Float)
    light = Column(Float)
    pressure = Column(Float)
    gas_quality = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

