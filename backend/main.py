
# main.py

from fastapi import FastAPI
from routes import plant_routes, photo_routes, sensor_routes, diagnosis_routes
from routes.plant_details import router as details_router
from routes.history_routes import router as history_router
from contextlib import asynccontextmanager
from fastapi.routing import APIRoute

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📋 Registered routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"✅ {route.path} → {route.name}")
    yield

print("Запуск main.py")

app = FastAPI(
     title="🌿 SunGreen API",
    description=(
        "AI-powered plant care assistant that helps you track plant health using:\n"
        "- Photos (analyzed by Gemini AI)\n"
        "- Sensor data (temperature, humidity, soil moisture, etc.)\n"
        "- Real-time weather data\n\n"
        "Features:\n"
        "- Watering schedule based on AI diagnosis\n"
        "- Daily watering reminders\n"
        "- Photo + sensor diagnosis options"
    ),
    version="1.0.0",
    contact={
        "name": "SunGreen",
        "email": "@gmail.com"
    },
    lifespan=lifespan
)


# ✅ Register all routers with the right prefixes
app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(photo_routes.router, prefix="/plants", tags=["Photos"])
app.include_router(sensor_routes.router, prefix="/plants", tags=["Sensors"])
app.include_router(diagnosis_routes.router, prefix="/diagnose", tags=["Diagnosis"])
app.include_router(details_router, prefix="/plants", tags=["Plant Details"])
app.include_router(history_router, prefix="/plants", tags=["History"])  # 💡 This matches with @router.get("/{plant_id}/history/...")

@app.get("/", tags=["System"])
def home():
    return {"message": "🌿 SunGreen API is up and running!"}


