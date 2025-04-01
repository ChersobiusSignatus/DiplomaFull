### services/weather.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

def get_weather_data(lat: float, lon: float) -> dict:
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}",
        "aqi": "no"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    return {
        "country": data["location"]["country"],
        "city": data["location"]["name"],
        "temp_c": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "heat_index_c": data["current"]["feelslike_c"],
        "uv_index": data["current"]["uv"]
    }