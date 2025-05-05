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

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Добавляем консольный обработчик, если его нет
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

@router.get("/{plant_id}/history/{selected_date}")
def get_plant_history_by_date(plant_id: UUID, selected_date: str, db: Session = Depends(get_db)):
    try:
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    logger.info(f"Запрос для plant_id={plant_id}, selected_date={selected_date}, parsed_date={parsed_date}")

    # Поиск записей за точную дату
    recommendation = db.query(Recommendation)\
        .filter(
            Recommendation.plant_id == plant_id,
            func.date(Recommendation.created_at) == parsed_date
        ).order_by(Recommendation.created_at.desc()).first()
    logger.info(f"Recommendation найдено: {recommendation is not None}, created_at: {recommendation.created_at if recommendation else 'None'}")

    sensor = db.query(SensorData)\
        .filter(
            SensorData.plant_id == plant_id,
            func.date(SensorData.created_at) == parsed_date
        ).order_by(SensorData.created_at.desc()).first()
    logger.info(f"Sensor найдено: {sensor is not None}, created_at: {sensor.created_at if sensor else 'None'}")

    photo = db.query(Photo)\
        .filter(
            Photo.plant_id == plant_id,
            func.date(Photo.created_at) == parsed_date
        ).order_by(Photo.created_at.desc()).first()
    logger.info(f"Photo найдено: {photo is not None}, created_at: {photo.created_at if photo else 'None'}")

    # Проверка на наличие данных
    if not recommendation and not sensor:
        logger.info("Данные не найдены, ищем ближайшие даты")
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

        detail = f"данных на {parsed_date} нет."
        if previous_date or next_date:
            detail += " Попробуйте"
            if previous_date:
                detail += f" {previous_date}"
            if previous_date and next_date:
                detail += " или"
            if next_date:
                detail += f" {next_date}"
        
        raise HTTPException(status_code=404, detail=detail)

    # Формирование ответа
    image_bytes = None
    if photo and photo.s3_url:
        try:
            image_response = requests.get(photo.s3_url)
            image_response.raise_for_status()
            image_bytes = image_response.content
        except:
            pass

    return Response(
        content=image_bytes or b"No image available",
        media_type="image/jpeg" if image_bytes else "text/plain",
        headers={
            "X-Recommendation": recommendation.content if recommendation else "Нет рекомендации",
            "X-Next-Watering": str(recommendation.next_watering) if recommendation and recommendation.next_watering else "",
            "X-Sensor-Temperature": str(sensor.temperature) if sensor else "",
            "X-Sensor-Humidity": str(sensor.humidity) if sensor else "",
            "X-Sensor-Light": str(sensor.light) if sensor else "",
            "X-Sensor-Soil": str(sensor.soil_moisture) if sensor else "",
            "X-Sensor-Gas": str(sensor.gas_quality) if sensor else ""
        }
    )