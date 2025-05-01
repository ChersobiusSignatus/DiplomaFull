from models.database import SessionLocal
from models.plant import Plant

db = SessionLocal()
plants = db.query(Plant).all()

for p in plants:
    print(p.id, p.name, p.last_watered, p.next_watering)
