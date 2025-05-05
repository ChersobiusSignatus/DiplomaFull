# routes/history_routes.py

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime
import requests
from fastapi.responses import Response
from models.recommendation import Recommendation
from models.database import get_db
from models.photo import Photo
from models.sensor_data import SensorData
import logging
import sys

print("Загрузка history_routes.py")

router = APIRouter()

# Настройка логирования для совместимости с uvicorn
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

logger.info("Загружен модуль history_routes.py")

@router.get("/{plant_id}/history/{selected_date}")
def get_plant_history_by_date(plant_id: UUID, selected_date: str, db: Session = Depends(get_db)):
    logger.info(f"Начало обработки запроса для plant_id={plant_id}, selected_date={selected_date}")
    try:
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        logger.info(f"Успешно распарсена дата: parsed_date={parsed_date}")
    except ValueError as e:
        logger.error(f"Ошибка парсинга даты: {e}, входная строка: {selected_date}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Поиск записей за точную дату
    try:
        recommendation = db.query(Recommendation)\
            .filter(
                Recommendation.plant_id == plant_id,
                func.date(Recommendation.created_at) == parsed_date
            ).order_by(Recommendation.created_at.desc()).first()
        logger.info(f"Recommendation найдено: {recommendation is not None}, created_at: {recommendation.created_at if recommendation else 'None'}")
    except Exception as e:
        logger.error(f"Ошибка при поиске recommendation: {e}")
        raise HTTPException(status_code=500, detail="Database error while fetching recommendation")

    try:
        sensor = db.query(SensorData)\
            .filter(
                SensorData.plant_id == plant_id,
                func.date(SensorData.created_at) == parsed_date
            ).order_by(SensorData.created_at.desc()).first()
        logger.info(f"Sensor найдено: {sensor is not None}, created_at: {sensor.created_at if sensor else 'None'}")
    except Exception as e:
        logger.error(f"Ошибка при поиске sensor: {e}")
        raise HTTPException(status_code=500, detail="Database error while fetching sensor")

    try:
        photo = db.query(Photo)\
            .filter(
                Photo.plant_id == plant_id,
                func.date(Photo.created_at) == parsed_date
            ).order_by(Photo.created_at.desc()).first()
        logger.info(f"Photo найдено: {photo is not None}, created_at: {photo.created_at if photo else 'None'}")
    except Exception as e:
        logger.error(f"Ошибка при поиске photo: {e}")
        raise HTTPException(status_code=500, detail="Database error while fetching photo")

    # Проверка на наличие данных
    if not recommendation and not sensor:
        logger.info("Данные не найдены, ищем ближайшие даты")
        try:
            previous_recommendation = db.query(Recommendation)\
                .filter(
                    Recommendation.plant_id == plant_id,
                    func.date(Recommendation.created_at) < parsed_date
                ).order_by(Recommendation.created_at.desc()).first()

            next_recommendation = db.query(Recommendation)\
                .filter(
                    Recommendation.plant_id == plant_id,
                    func.date(Recommendation.created_at) > parsed_date
                ).order_by(Recommendation.created_at.asc()).first()

            previous_date = previous_recommendation.created_at.date().strftime("%Y-%m-%d") if previous_recommendation else None
            next_date = next_recommendation.created_at.date().strftime("%Y-%m-%d") if next_recommendation else None

            detail = f"No data for {parsed_date}."  # Используем ASCII-совместимую строку
            if previous_date or next_date:
                detail += " Try"
                if previous_date:
                    detail += f" {previous_date}"
                if previous_date and next_date:
                    detail += " or"
                if next_date:
                    detail += f" {next_date}"
            logger.info(f"Returning 404 with message: {detail}")
            raise HTTPException(status_code=404, detail=detail)
        except Exception as e:
            logger.error(f"Error while searching for nearest dates: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    logger.info("Data found, forming response")
    # Формирование ответа
    image_bytes = None
    if photo and photo.s3_url:
        try:
            image_response = requests.get(photo.s3_url)
            image_response.raise_for_status()
            image_bytes = image_response.content
        except Exception as e:
            logger.error(f"Error downloading photo: {e}")

    # Убедимся, что все значения заголовков — ASCII-совместимые строки
    headers = {
        "X-Recommendation": str(recommendation.content) if recommendation else "No recommendation",
        "X-Next-Watering": str(recommendation.next_watering) if recommendation and recommendation.next_watering else "",
        "X-Sensor-Temperature": str(sensor.temperature) if sensor else "",
        "X-Sensor-Humidity": str(sensor.humidity) if sensor else "",
        "X-Sensor-Light": str(sensor.light) if sensor else "",
        "X-Sensor-Soil": str(sensor.soil_moisture) if sensor else "",
        "X-Sensor-Gas": str(sensor.gas_quality) if sensor else ""
    }

    return Response(
        content=image_bytes or b"No image available",
        media_type="image/jpeg" if image_bytes else "text/plain",
        headers=headers
    )