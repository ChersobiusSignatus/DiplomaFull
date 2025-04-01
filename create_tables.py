# create_tables.py
from models.database import engine, Base
from models import plant, photo, sensor_data, recommendation

print("🔨 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")
