
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is not set!")

plant_id = "7c721d41-ad67-46b3-a998-bfad5abe63e8"
selected_date = "2025-04-25"

print(f"\n🔎 Проверка данных на дату {selected_date} для plant_id = {plant_id}\n")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Проверка рекомендаций
    print("📘 Рекомендации:")
    cursor.execute("""
        SELECT id, type, content, created_at 
        FROM recommendations 
        WHERE plant_id = %s AND DATE(created_at) = %s
    """, (plant_id, selected_date))
    recommendations = cursor.fetchall()
    if recommendations:
        for row in recommendations:
            print(dict(row))
    else:
        print("Нет рекомендаций на эту дату.")

    # Проверка сенсоров
    print("\n🌡️ Сенсорные данные:")
    cursor.execute("""
        SELECT id, temperature, humidity, light, soil_moisture, gas_quality, created_at 
        FROM sensor_data 
        WHERE plant_id = %s AND DATE(created_at) = %s
    """, (plant_id, selected_date))
    sensors = cursor.fetchall()
    if sensors:
        for row in sensors:
            print(dict(row))
    else:
        print("Нет сенсорных данных на эту дату.")

except Exception as e:
    print(f"🚨 Ошибка: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
