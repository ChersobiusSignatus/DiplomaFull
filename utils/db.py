# utils/db.py

from sqlalchemy.orm import Session
from models.database import SessionLocal

# ✅ Получение сессии БД через контекстный генератор
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
