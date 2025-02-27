from models.database import Base, engine
from models.vision_analysis import VisionAnalysis
import logging

try:
    print("⏳ Создаем таблицы в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы!")
except Exception as e:
    logging.error(f"Ошибка создания таблиц: {str(e)}")
