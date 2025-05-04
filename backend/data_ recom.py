from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.recommendation import Recommendation
from models.sensor_data import SensorData
from uuid import UUID
from datetime import datetime, date

plant_id = UUID("7c721d41-ad67-46b3-a998-bfad5abe63e8")
target_date = date(2025, 4, 25)

db: Session = SessionLocal()

print("\nRecommendations:")
for rec in db.query(Recommendation).filter(Recommendation.plant_id == plant_id).all():
    print("-", rec.created_at, rec.content)

print("\nSensorData:")
for s in db.query(SensorData).filter(SensorData.plant_id == plant_id).all():
    print("-", s.created_at, s.temperature, s.soil_moisture)

db.close()


