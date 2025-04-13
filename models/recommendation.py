#models/recommendation.py
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid
from .database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    type = Column(String, nullable=False)  # 'photo' or 'combined'
    content = Column(String, nullable=False)  # Gemini's response
    created_at = Column(DateTime, default=datetime.utcnow)


