import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

if not WEATHER_API_KEY:
    raise ValueError("❌ WEATHER_API_KEY is missing in your .env file.")

# 🧠 Простое in-memory кеш-хранилище
_weather_cache = {}
CACHE_DURATION = timedelta(hours=4)


def get_weather_data(lat: float, lon: float) -> dict:
    key = f"{lat:.3f},{lon:.3f}"
    now = datetime.utcnow()

    # ✅ Проверяем кеш
    if key in _weather_cache:
        cached = _weather_cache[key]
        if now - cached["timestamp"] < CACHE_DURATION:
            return cached["data"]

    # 🛰️ Делаем реальный запрос
    params = {
        "key": WEATHER_API_KEY,
        "q": key,
        "aqi": "no"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    result = {
        "country": data["location"]["country"],
        "city": data["location"]["name"],
        "temp_c": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "heat_index_c": data["current"]["feelslike_c"],
        "uv_index": data["current"]["uv"]
    }

    # 🧠 Сохраняем в кеш
    _weather_cache[key] = {
        "timestamp": now,
        "data": result
    }

    return result
