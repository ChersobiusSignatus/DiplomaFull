# services/gemini.py
from datetime import datetime
import os
import json
import requests
import base64
import re
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# 🔐 API config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL") or \
    "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-pro-vision:generateContent"

headers = {
    "Content-Type": "application/json"
}

# 📤 Gemini API call without image (for text-only prompts)
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

# 📤 Gemini API call with image data (image must be in bytes)
def call_gemini_api_with_image(image_bytes: bytes, prompt: str) -> str:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
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

# 📥 Parse Gemini response (fallback if JSON fails)
def parse_gemini_json_response(response: str) -> dict:
    try:
        data = json.loads(response)
        return {
            "recommendation": data.get("recommendation", response),
            "next_watering_in_days": data.get("next_watering_in_days", 3),
            "next_watering_date": data.get("next_watering_date")
        }
    except json.JSONDecodeError:
        match = re.search(r"(\d{4}-\d{2}-\d{2})", response)
        return {
            "recommendation": response,
            "next_watering_in_days": 3,
            "next_watering_date": match.group(1) if match else None
        }


# 🧠 Prompt for image-based analysis
def get_photo_prompt(
    plant_name: str,
    plant_type: str,
    previous_interval: Optional[int] = None,
    last_watered: Optional[datetime] = None
) -> str:
    memory_parts = []
    if previous_interval:
        memory_parts.append(f"Ранее рекомендованный интервал полива: {previous_interval} дней.")
    if last_watered:
        memory_parts.append(f"Последний полив был: {last_watered.strftime('%Y-%m-%d')}.")

    memory = "\n".join(memory_parts)

    return f"""
Ты — специалист по здоровью растений. Проанализируй фотографию растения по имени \"{plant_name}\" (тип: {plant_type}).

Обрати внимание на признаки заболеваний, обезвоживания или стресса.

{memory}

Верни JSON объект со следующими полями:
- \"recommendation\": советы по уходу
- \"next_watering_in_days\": через сколько дней полить
- \"next_watering_date\": следующая дата полива в формате YYYY-MM-DD

Пример:
{{
  "recommendation": "Растение показывает признаки стресса от солнца. Уберите его в тень. Следующий полив через 4 дня.",
  "next_watering_in_days": 4,
  "next_watering_date": "2025-04-25"
}}
"""

# 🧠 Prompt for combined sensor + image + weather analysis
def get_combined_prompt(
    plant_name: str,
    plant_type: str,
    sensors,
    weather: dict = None,
    previous_interval: Optional[int] = None,
    last_watered: Optional[datetime] = None
) -> str:
    memory = []
    if previous_interval:
        memory.append(f"Ранее рекомендованный интервал полива: {previous_interval} дней.")
    if last_watered:
        memory.append(f"Последний полив был: {last_watered.strftime('%Y-%m-%d')}.")

    memory_block = "\n".join(memory)

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
Ты — специалист по уходу за растениями. Проанализируй данные сенсоров и предложи рекомендации по уходу за растением {plant_name}, тип: {plant_type}.

{memory_block}

Данные с сенсоров:
- Температура: {sensors.temperature}°C
- Влажность воздуха: {sensors.humidity}%
- Влажность почвы: {sensors.soil_moisture}
- Освещённость: {sensors.light} люкс
- Качество воздуха (газа): {sensors.gas_quality}
{weather_part}

Верни JSON объект со следующими полями:
- \"recommendation\": рекомендации по уходу
- \"next_watering_in_days\": через сколько дней полить
- \"next_watering_date\": следующая дата полива в формате YYYY-MM-DD

Пример:
{{
  "recommendation": "Исходя из всех данных: Влажность почвы низкая, слишком много света. Полейте сегодня и снова через 3 дня. Уберите растение в тень",
  "next_watering_in_days": 3,
  "next_watering_date": "2025-04-25"
}}
"""
