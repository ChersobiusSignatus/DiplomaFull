### services/storage.py
import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_to_s3(file):
    file_extension = file.filename.split(".")[-1]
    filename = f"plant_photos/{uuid.uuid4()}.{file_extension}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs={"ACL": "public-read"})
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"


