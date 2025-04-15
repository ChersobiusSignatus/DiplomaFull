# services/storage.py

import boto3
import uuid
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# 🔐 Получаем переменные из .env
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# 🧠 Проверка, что все ключи есть
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME]):
    raise ValueError("❌ Missing AWS S3 credentials in .env file.")

# ✅ Инициализация клиента S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file) -> str:
    file_extension = file.filename.split(".")[-1].lower()
    filename = f"plant_photos/{uuid.uuid4()}.{file_extension}"

    s3.upload_fileobj(
        file.file,
        S3_BUCKET_NAME,
        filename
    )

    public_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return public_url
