from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

# Google Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = "your_api_key_here"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

@app.get("/")
def home():
    return {"message": "Plant Health API is running!"}

# Endpoint to upload image and analyze plant health
@app.post("/analyze/")
async def analyze_plant(image: UploadFile = File(...)):
    image_data = await image.read()

    # Send image to Gemini API
    response = requests.post(GEMINI_API_URL, files={"file": image_data})

    if response.status_code == 200:
        result = response.json()
        return {"status": "success", "data": result}
    else:
        return {"status": "error", "message": "Failed to analyze image"}

