# drop_all_data.py
from models.database import SessionLocal
from models.plant import Plant
from models.photo import Photo
from models.sensor_data import SensorData
from models.recommendation import Recommendation
from sqlalchemy.orm import Session

def delete_all_data(db: Session):
    db.query(Recommendation).delete()
    db.query(SensorData).delete()
    db.query(Photo).delete()
    db.query(Plant).delete()
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        delete_all_data(db)
        print("✅ Все записи успешно удалены.")
    finally:
        db.close()
