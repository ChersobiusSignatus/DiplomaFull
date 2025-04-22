# services/gemini.py

from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv
from typing import Optional
import base64

load_dotenv()

# 🔐 API config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL") or \
    "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-pro-vision:generateContent"

headers = {
    "Content-Type": "application/json"
}

def call_gemini_api(prompt: str) -> str:
    body = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nПожалуйста, ответь на русском языке."}]}]
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=body
    )
    response.raise_for_status()
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def call_gemini_api_with_image(image_bytes: bytes, prompt: str) -> str:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "text": f"{prompt}\n\nПожалуйста, ответь на русском языке."
                    }
                ]
            }
        ]
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
            "next_watering_in_days": 3,
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
        memory_parts.append(f"Последний рекомендованный интервал полива был {previous_interval} дней.")
    if last_watered:
        memory_parts.append(f"Последний полив был {last_watered.strftime('%Y-%m-%d')}.")

    memory = "\n".join(memory_parts)

    return f"""
Ты — эксперт по уходу за растениями. Проанализируй изображение растения по имени "{plant_name}" (тип: {plant_type}).
Ищи признаки болезни, обезвоживания или стресса.

{memory}

Верни JSON-объект:
- "recommendation": твоя рекомендация по уходу
- "next_watering_in_days": через сколько дней поливать
- "next_watering_date": точная дата в формате YYYY-MM-DD

Пример:
{{
  "recommendation": "Растение выглядит здоровым. Следующий полив через 4 дня.",
  "next_watering_in_days": 4,
  "next_watering_date": "2025-04-25"
}}
"""

def get_combined_prompt(plant_name: str, sensors, weather: dict = None, previous_interval: Optional[int] = None) -> str:
    memory = f"Последний рекомендованный интервал полива был {previous_interval} дней.\n" if previous_interval else ""

    weather_part = ""
    if weather:
        weather_part = f"""
Данные о погоде:
- Местоположение: {weather['city']}, {weather['country']}
- Температура: {weather['temp_c']}°C
- Влажность: {weather['humidity']}%
- Индекс жары: {weather['heat_index_c']}°C
- УФ-индекс: {weather['uv_index']}
"""

    return f"""
Ты — специалист по уходу за растениями. На основе этих данных дай рекомендации по уходу за растением "{plant_name}".

{memory}

Показания сенсоров:
- Температура: {sensors.temperature}°C
- Влажность воздуха: {sensors.humidity}%
- Влажность почвы: {sensors.soil_moisture}
- Освещенность: {sensors.light} lux
- Качество воздуха: {sensors.gas_quality}
{weather_part}

Верни JSON-объект:
- "recommendation": твоя рекомендация
- "next_watering_in_days": через сколько дней поливать
- "next_watering_date": точная дата в формате YYYY-MM-DD

Пример:
{{
  "recommendation": "Почва сухая, рекомендуется полив сегодня и повторный через 3 дня.",
  "next_watering_in_days": 3,
  "next_watering_date": "2025-04-25"
}}
"""
