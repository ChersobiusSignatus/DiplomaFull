import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
# Read values from .env
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET_NAME]):
    raise ValueError("❌ Missing AWS credentials! Check your .env file.")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Set it in the .env file.")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Set it in the .env file.")
