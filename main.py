# main.py
from fastapi import FastAPI
from routes import plant_routes, photo_routes, diagnosis_routes, sensor_routes

app = FastAPI(title="🌿 Plant Health API")

# Include routers
app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(photo_routes.router, prefix="/plants", tags=["Photos"])
app.include_router(diagnosis_routes.router, prefix="/diagnose", tags=["Diagnosis"])
app.include_router(sensor_routes.router, prefix="/plants", tags=["Sensor Data"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Health API 🌱"}
