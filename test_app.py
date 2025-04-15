import pytest
from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_plant():
    response = client.post("/plants/", json={
        "name": "Test Plant",
        "type": "aloe",
        "last_watered": None
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Plant"
    global plant_id
    plant_id = response.json()["id"]


def test_upload_photo():
    test_create_plant()  # Ensure plant_id is defined
    with open("test_image.jpg", "rb") as file:
        response = client.post(f"/plants/{plant_id}/photos", files={"file": ("test_image.jpg", file, "image/jpeg")})
    assert response.status_code == 200
    assert response.json()["is_current"] is True


def test_upload_sensor_data():
    response = client.post(f"/plants/{plant_id}/sensor-data", json={
        "temperature": 25.0,
        "humidity": 50.0,
        "soil_moisture": 300.0,
        "light": 15000.0,
        
        "gas_quality": 0.85
    })
    assert response.status_code == 200
    assert "temperature" in response.json()


def test_water_and_trigger_diagnosis():
    response = client.post(f"/plants/{plant_id}/water")
    assert response.status_code == 200
    assert "recommendation" in response.json()


def test_get_watering_today():
    response = client.get("/plants/watering-today")
    assert response.status_code == 200
    assert isinstance(response.json(), list)