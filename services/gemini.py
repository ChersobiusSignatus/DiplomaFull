# services/gemini.py

from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# 🔐 API config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL") or \
    "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json"
}

def call_gemini_api(prompt: str) -> str:
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=body
    )
    response.raise_for_status()
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def parse_gemini_json_response(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "recommendation": response,
            "next_watering_in_days": 3,  # fallback значение
            "next_watering_date": None
        }

def get_photo_prompt(
    plant_name: str,
    plant_type: str,
    previous_interval: Optional[int] = None,
    last_watered: Optional[datetime] = None
) -> str:
    memory_parts = []

    if previous_interval:
        memory_parts.append(f"The last recommended watering interval was {previous_interval} days.")
    if last_watered:
        memory_parts.append(f"The plant was last watered on {last_watered.strftime('%Y-%m-%d')}.")

    memory = "\n".join(memory_parts)

    return f"""
You are a plant health expert. Analyze the photo of a plant named \"{plant_name}\", which is a {plant_type}.

Look for signs of disease, dehydration, or stress.

{memory}

Return a JSON object with:
- \"recommendation\": your care advice
- \"next_watering_in_days\": integer
- \"next_watering_date\": YYYY-MM-DD

Example:
{{
  "recommendation": "The plant looks healthy. Water it again in 4 days.",
  "next_watering_in_days": 4,
  "next_watering_date": "2025-04-25"
}}
"""

def get_combined_prompt(plant_name: str, sensors, weather: dict = None, previous_interval: Optional[int] = None) -> str:
    memory = f"The last recommended watering interval was {previous_interval} days.\n" if previous_interval else ""

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
You are a plant care specialist. Based on this information, recommend the ideal care routine for the {plant_name}.

{memory}

Sensor Data:
- Temperature: {sensors.temperature}°C
- Humidity: {sensors.humidity}%
- Soil Moisture: {sensors.soil_moisture}
- Light: {sensors.light} lux
- Gas Quality: {sensors.gas_quality}
{weather_part}

Return a JSON object with:
- \"recommendation\": care advice
- \"next_watering_in_days\": integer
- \"next_watering_date\": YYYY-MM-DD

Example:
{{
  "recommendation": "Moisture is low. Water now and again in 3 days.",
  "next_watering_in_days": 3,
  "next_watering_date": "2025-04-25"
}}
"""
