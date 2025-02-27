import google.generativeai as genai
import base64
import json
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image_with_gemini(image_data, mime_type):
    """Анализ изображения с помощью Gemini AI."""
    
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": "Определи состояние растения по изображению. "
                             "Ответ должен быть в JSON формате: "
                             '{"diagnosis": "здоровое растение" или "название болезни", '
                             '"recommendation": "рекомендация по уходу"}'},
                    {"inline_data": {"mime_type": mime_type, "data": image_base64}}
                ]
            }
        ]
    }

    model = genai.GenerativeModel("gemini-2.0")
    response = model.generate_content(payload)

    try:
        return json.loads(response.text)  # Декодируем JSON-ответ
    except Exception:
        return {"status": "error", "message": "Ошибка анализа изображения"}
