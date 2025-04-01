# drop_tables.py
from models.database import Base, engine

print("⚠️ Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("✅ All tables dropped.")
