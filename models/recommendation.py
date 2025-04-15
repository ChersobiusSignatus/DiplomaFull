# models/recommendation.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)

    type = Column(String, nullable=False)   # "photo" или "combined"
    content = Column(String, nullable=False)  # Текст от Gemini (JSON-структура или текст)
    created_at = Column(DateTime, default=datetime.utcnow)
