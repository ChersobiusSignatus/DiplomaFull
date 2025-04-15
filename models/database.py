# models/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# ✅ Загружаем переменные окружения
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing in your .env file.")

# ✅ Создаём движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # автоматически проверяет соединение
)

# ✅ Сессия для работы с БД
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ✅ Базовый класс для всех моделей
Base = declarative_base()

# ✅ Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

