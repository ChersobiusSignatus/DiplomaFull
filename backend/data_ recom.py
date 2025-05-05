
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from uuid import UUID

# Настройки подключения к базе данных
# Замените параметры на свои: имя пользователя, пароль, хост, порт и имя базы данных
DATABASE_URL = "postgresql://postgres:Kogp9He!gds@database-1.ctm2g2is8193.eu-central-1.rds.amazonaws.com:5432/helth_db"


# Создаём подключение к базе данных
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# ID растения
plant_id = "7c721d41-ad67-46b3-a998-bfad5abe63e8"

try:
    # 1. Проверка таблицы recommendations
    print("Проверка таблицы recommendations:")
    result = db.execute(
        text("SELECT created_at FROM recommendations WHERE plant_id = :plant_id"),
        {"plant_id": plant_id}
    )
    recommendations = result.fetchall()
    if recommendations:
        for row in recommendations:
            print(f"recommendations.created_at: {row[0]}")
    else:
        print("Записей в recommendations не найдено.")

    # 2. Проверка таблицы sensor_data
    print("\nПроверка таблицы sensor_data:")
    result = db.execute(
        text("SELECT created_at FROM sensor_data WHERE plant_id = :plant_id"),
        {"plant_id": plant_id}
    )
    sensor_data = result.fetchall()
    if sensor_data:
        for row in sensor_data:
            print(f"sensor_data.created_at: {row[0]}")
    else:
        print("Записей в sensor_data не найдено.")

    # 3. Проверка таблицы photos
    print("\nПроверка таблицы photos:")
    result = db.execute(
        text("SELECT * FROM photos WHERE plant_id = :plant_id"),
        {"plant_id": plant_id}
    )
    photos = result.fetchall()
    if photos:
        for row in photos:
            print(f"photos: {row}")
    else:
        print("Записей в photos не найдено.")

except Exception as e:
    print(f"Произошла ошибка при выполнении запросов: {e}")

finally:
    # Закрываем сессию
    db.close()