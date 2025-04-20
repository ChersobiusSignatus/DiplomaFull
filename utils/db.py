# utils/db.py

from sqlalchemy.orm import Session
from models.database import SessionLocal
from typing import Generator

# ✅ Получение сессии БД через контекстный генератор
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
