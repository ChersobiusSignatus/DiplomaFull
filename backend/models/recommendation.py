# models/recommendation.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Связи
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"), nullable=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensor_data.id"), nullable=True)

    # Основные данные
    type = Column(String, nullable=False)  # "photo" или "combined"
    content = Column(String, nullable=False)  # Ответ от Gemini

    # Полив
    last_watered = Column(DateTime, nullable=True)
    next_watering = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
