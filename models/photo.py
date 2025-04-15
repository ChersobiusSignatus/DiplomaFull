# models/photo.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    s3_url = Column(String, nullable=False)
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
