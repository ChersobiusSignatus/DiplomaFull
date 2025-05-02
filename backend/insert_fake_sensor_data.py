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
        temperature=27.2,
        humidity=32.0,
        soil_moisture=17.4,
        light=9500.0,
        gas_quality=0.69,
        created_at=datetime(2025, 5, 2, 12, 0)
    )

    with Session(engine) as session:
        session.add(entry)
        session.commit()
        print(f"✅ Inserted for {entry.created_at.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    insert_fake_sensor_data()
