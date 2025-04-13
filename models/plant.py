### models/plant.py

import datetime
from sqlalchemy import Column, String, DateTime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID

import uuid
from .database import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)         # User-defined name
    type = Column(String, nullable=False)         # Predefined plant type
    created_at = Column(DateTime, default=datetime.utcnow)


