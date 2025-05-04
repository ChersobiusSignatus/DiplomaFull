
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from models.database import Base, get_db
from models.recommendation import Recommendation
from models.sensor_data import SensorData
from uuid import UUID
from datetime import datetime, time


import os
import psycopg2
from datetime import date

# 🔧 Укажи свои данные подключения
DATABASE_URL = ""

plant_id = "7c721d41-ad67-46b3-a998-bfad5abe63e8"
selected_date = date(2025, 4, 25)

tables = {
    "recommendations": "created_at",
    "sensor_data": "created_at",
    "photos": "created_at"
}

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    for table, time_column in tables.items():
        print(f"\n🔍 {table.upper()}:")

        cursor.execute(f"""
            SELECT id, {time_column}
            FROM {table}
            WHERE plant_id = %s AND DATE({time_column}) = %s
            ORDER BY {time_column} ASC
        """, (plant_id, selected_date))

        rows = cursor.fetchall()
        if not rows:
            print("  ⛔ Нет данных.")
        else:
            for row in rows:
                print(f"  ✅ ID: {row[0]}, created_at: {row[1].isoformat()}")

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
