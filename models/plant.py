# models/plant.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)          # Пользовательское имя растения
    type = Column(String, nullable=False)          # aloe, cactus, ficus и т.д.
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Новые поля
    last_watered = Column(DateTime, nullable=True)        # Когда пользователь поливал вручную
    next_watering = Column(DateTime, nullable=True)       # Дата следующего полива от Gemini
