# insert_fake_sensor_data.py

import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import engine
from models.sensor_data import SensorData

def insert_fake_sensor_data():
    plant_id = "7c721d41-ad67-46b3-a998-bfad5abe63e8"

    entry = SensorData(
        id=uuid.uuid4(),
        plant_id=plant_id,
        temperature=18.4,       # прохладно
        humidity=89.0,          # высокая влажность воздуха
        soil_moisture=42.3,     # влажная почва после дождя
        light=1800.0,           # слабое освещение из-за облачности
        gas_quality=0.73,       # немного хуже, из-за сырости
        created_at=datetime(2025, 5, 3, 12, 0)  # 3 мая в полдень
    )

    with Session(engine) as session:
        session.add(entry)
        session.commit()
        print(f"✅ Inserted for {entry.created_at.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    insert_fake_sensor_data()
