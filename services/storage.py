import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError
from utils.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME

# Инициализируем клиент S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(image_data, filename):
    """Загружает изображение в AWS S3 и возвращает URL"""
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType="image/jpeg"
        )
        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
    except NoCredentialsError:
        logging.error("❌ AWS Credentials not found!")
        return None
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки в AWS S3: {e}")
        return None
