from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from .database import Base

class VisionAnalysis(Base):
    __tablename__ = "vision_analysis"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())


