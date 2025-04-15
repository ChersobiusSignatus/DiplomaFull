# utils/config.py

import os
from dotenv import load_dotenv

# 🔄 Загружаем переменные окружения из .env
load_dotenv()

# 🌱 PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# ☁️ AWS S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# 🤖 Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")  # по умолчанию задаётся в gemini.py

# 🌦️ Weather API
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ✅ Проверка на наличие критичных переменных
required_vars = {
    "DATABASE_URL": DATABASE_URL,
    "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
    "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
    "AWS_REGION": AWS_REGION,
    "S3_BUCKET_NAME": S3_BUCKET_NAME,
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "WEATHER_API_KEY": WEATHER_API_KEY
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise ValueError(f"❌ Missing required environment variables: {', '.join(missing)}")
