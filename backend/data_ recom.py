
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from models.database import Base, get_db
from models.recommendation import Recommendation
from models.sensor_data import SensorData
from uuid import UUID
from datetime import datetime, time


plant_id = UUID("7c721d41-ad67-46b3-a998-bfad5abe63e8")
target_date = datetime.strptime("2025-04-25", "%Y-%m-%d").date()

start_dt = datetime.combine(target_date, time.min)
end_dt = datetime.combine(target_date, time.max)

engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    print("\n📌 Проверяем Recommendation:")
    rec = session.query(Recommendation).filter(
        and_(
            Recommendation.plant_id == plant_id,
            Recommendation.created_at >= start_dt,
            Recommendation.created_at <= end_dt
        )
    ).all()
    for r in rec:
        print(f"- {r.created_at} | {r.content}")

    print("\n📌 Проверяем SensorData:")
    sensors = session.query(SensorData).filter(
        and_(
            SensorData.plant_id == plant_id,
            SensorData.created_at >= start_dt,
            SensorData.created_at <= end_dt
        )
    ).all()
    for s in sensors:
        print(f"- {s.created_at} | Temp: {s.temperature} | Soil: {s.soil_moisture}")
