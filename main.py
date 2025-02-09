import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Load environment variables from .env file
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

    # Send the image to Gemini API
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    response = requests.post(GEMINI_API_URL, files={"file": image_data}, headers=headers)

    # Handle API response
    if response.status_code == 200:
        result = response.json()
        return JSONResponse(content={"status": "success", "data": result})
    else:
        return JSONResponse(content={"status": "error", "message": "Failed to analyze image"}, status_code=response.status_code)
