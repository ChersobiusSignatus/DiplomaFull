from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class PlantAnalysis(Base):
    __tablename__ = "plant_analysis"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

Base.metadata.create_all(bind=engine)
