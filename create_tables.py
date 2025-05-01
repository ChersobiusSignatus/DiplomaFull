# create_tables.py

from models.database import engine, Base
from models import plant, photo, sensor_data, recommendation

def create_all_tables():
    print("🔨 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
