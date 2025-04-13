### services/gemini.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL") or "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

headers = {
    "Content-Type": "application/json"
}

def call_gemini_api(prompt: str) -> str:
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def get_photo_prompt(plant_name: str) -> str:
    return f"""
You are a plant health expert. Analyze this plant's condition based on the uploaded photo of a {plant_name}.
The image may show signs of disease, dehydration, or other issues. Provide a diagnosis and actionable care advice.
"""

def get_combined_prompt(plant_name: str, sensors, weather: dict = None) -> str:
    weather_part = ""
    if weather:
        weather_part = f"""
Weather Data:
- Location: {weather['city']}, {weather['country']}
- Temperature: {weather['temp_c']}°C
- Humidity: {weather['humidity']}%
- Heat Index: {weather['heat_index_c']}°C
- UV Index: {weather['uv_index']}
"""

    return f"""
You're a plant care specialist. Based on the following information, provide care recommendations for a {plant_name}:

Photo: An image of the plant is available.
Sensor Readings:
- Temperature: {sensors.temperature}°C
- Humidity: {sensors.humidity}%
- Light: {sensors.light} lux
- Moisture: {sensors.soil_moisture}
- Air Quality: {sensors.gas_quality}
{weather_part}

Consider ideal growing conditions for this plant and suggest what should be done to maintain or improve its health.
"""


