from fastapi import FastAPI
from routes.analyze import router as analyze_router

app = FastAPI()

# Include routes
app.include_router(analyze_router)

@app.get("/")
def home():
    return {"message": "Plant Health API is running with Gemini 2.0 Flash!"}
