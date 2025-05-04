from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.recommendation import Recommendation
from models.database import Base  # Импортируй как у тебя
import os

# Убедись, что .env или config.py содержит DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание подключения
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Искомый plant_id
plant_id = "7c721d41-ad67-46b3-a998-bfad5abe63e8"

# Получение всех рекомендаций
recommendations = session.query(Recommendation)\
    .filter(Recommendation.plant_id == plant_id)\
    .order_by(Recommendation.created_at.desc())\
    .all()

# Вывод
for rec in recommendations:
    print(f"🪴 Date: {rec.created_at}")
    print(f"📷 Photo ID: {rec.photo_id}")
    print(f"📡 Sensor ID: {rec.sensor_id}")
    print(f"💬 Type: {rec.type}")
    print(f"📝 Recommendation:\n{rec.content}")
    print(f"💧 Last watered: {rec.last_watered}")
    print(f"🚿 Next watering: {rec.next_watering}")
    print("-" * 50)

session.close()
