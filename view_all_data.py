from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# ✅ Загрузить переменные окружения
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Подключение к базе
engine = create_engine(DATABASE_URL)

# ✅ Таблицы для просмотра
tables = ["plants", "photos", "sensor_data", "recommendations"]

with engine.connect() as conn:
    for table in tables:
        print(f"\n📄 {table.upper()}:\n" + "-" * 40)
        result = conn.execute(text(f"SELECT * FROM {table}"))
        rows = result.fetchall()
        if not rows:
            print("❌ No data found.")
        else:
            for row in rows:
                print(dict(row))
