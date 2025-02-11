import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import base64
from google.cloud import storage

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load API Key securely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please set it in the .env file.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

@app.get("/")
def home():
    return {"message": "Plant Health API is running!"}

@app.post("/analyze/")
async def analyze_plant(image: UploadFile = File(...)):
    """Handles plant image uploads and sends them to Gemini API for analysis."""
    
    # Read image data
    image_data = await image.read()

    # Check if image is empty
    if not image_data:
        raise HTTPException(status_code=400, detail="No image provided")

    # Convert image to Base64 for Gemini API
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    # Request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": image.content_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    # Send request to Gemini API
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    # Handle API response
    if response.status_code == 200:
        result = response.json()
        return JSONResponse(content={"status": "success", "data": result})
    else:
        return JSONResponse(content={"status": "error", "message": "Failed to analyze image"}, status_code=response.status_code)



# Load environment variables
GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize Google Cloud Storage client
storage_client = storage.Client.from_service_account_json(GCP_CREDENTIALS)
bucket = storage_client.bucket(BUCKET_NAME)

def upload_to_gcs(image_data, filename):
    """Uploads image to Google Cloud Storage and returns the file URL."""
    blob = bucket.blob(filename)
    blob.upload_from_string(image_data, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    """Uploads image to Google Cloud Storage and returns the URL."""
    image_data = await image.read()
    
    if not image_data:
        raise HTTPException(status_code=400, detail="No image provided")

    filename = f"plants/{image.filename}"
    image_url = upload_to_gcs(image_data, filename)

    return {"status": "success", "image_url": image_url}


from sqlalchemy.orm import Session
from models import SessionLocal, PlantAnalysis

def save_analysis_result(image_url, diagnosis, recommendation):
    """Saves analysis result to the database."""
    db: Session = SessionLocal()
    new_entry = PlantAnalysis(
        image_url=image_url,
        diagnosis=diagnosis,
        recommendation=recommendation
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()

@app.post("/analyze/")
async def analyze_plant(image: UploadFile = File(...)):
    """Uploads image, analyzes plant health, and stores results."""
    
    # Upload image to Google Cloud Storage
    image_data = await image.read()
    filename = f"plants/{image.filename}"
    image_url = upload_to_gcs(image_data, filename)

    # Process image with Gemini API
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    payload = {"contents": [{"parts": [{"inline_data": {"mime_type": image.content_type, "data": image_base64}}]}]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        diagnosis = result.get("diagnosis", "Unknown condition")
        recommendation = result.get("recommendation", "No recommendation available")
        
        # Save to database
        save_analysis_result(image_url, diagnosis, recommendation)
        
        return {"status": "success", "image_url": image_url, "diagnosis": diagnosis, "recommendation": recommendation}
    
    return {"status": "error", "message": "Failed to analyze image"}
