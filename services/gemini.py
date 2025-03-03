import google.generativeai as genai
import base64
import json
import logging
from utils.config import GEMINI_API_KEY

# Настроим логирование
logging.basicConfig(level=logging.DEBUG)

# Настройка API-ключа
genai.configure(api_key=GEMINI_API_KEY)

# Используем правильное название модели с "models/"
MODEL_NAME = "models/gemini-2.0-flash"

def check_available_models():
    """Функция для проверки доступных моделей."""
    try:
        available_models = genai.list_models()
        model_names = [model.name for model in available_models]
        logging.debug(f"📌 Доступные модели: {model_names}")
        if MODEL_NAME not in model_names:
            logging.error(f"❌ Модель {MODEL_NAME} не найдена! Используй одну из доступных: {model_names}")
            return False
        return True
    except Exception as e:
        logging.error(f"❌ Ошибка при получении списка моделей: {str(e)}")
        return False

def analyze_image_with_gemini(image_data, mime_type):
    """Отправляет изображение в Gemini AI и получает результат анализа."""
    
    # Проверяем, доступна ли модель
    if not check_available_models():
        return {"status": "error", "message": f"Модель {MODEL_NAME} не найдена. Проверь список доступных моделей."}

    image_base64 = base64.b64encode(image_data).decode("utf-8")

    model = genai.GenerativeModel(MODEL_NAME)

    payload = {
        "parts": [
            {
                "text": "Определи состояние растения по изображению. "
                        "Ответ должен быть в JSON формате: "
                        '{"diagnosis": "здоровое растение" или "название болезни", '
                        '"recommendation": "рекомендация по уходу"}'
            },
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_base64
                }
            }
        ]
    }

    try:
        response = model.generate_content(payload)

        # Логируем, что вернул Gemini
        logging.debug(f"🔍 Ответ от Gemini (сырые данные): {response.text}")

        if response and response.text:
            # Пробуем разобрать JSON
            try:
                parsed_response = json.loads(response.text)
                return parsed_response
            except json.JSONDecodeError:
                logging.error("❌ Ошибка декодирования JSON от Gemini")
                return {"status": "error", "message": "Ошибка анализа изображения. Некорректный JSON."}
        else:
            return {"status": "error", "message": "Ошибка анализа изображения. Пустой ответ от Gemini."}
    
    except Exception as e:
        logging.error(f"❌ Ошибка отправки запроса в Gemini: {str(e)}")
        return {"status": "error", "message": f"Ошибка запроса в Gemini: {str(e)}"}
