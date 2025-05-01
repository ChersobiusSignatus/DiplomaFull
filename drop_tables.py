# drop_tables.py

from models.database import engine, Base
from models import plant, photo, sensor_data, recommendation

def drop_all_tables():
    print("⚠️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped.")

if __name__ == "__main__":
    drop_all_tables()
