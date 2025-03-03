import logging
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from services.gemini import analyze_image_with_gemini
from services.storage import upload_to_s3
from services.db_operations import save_analysis_result
from models.database import get_db

# Настроим логирование
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

@router.post("/analyze/")
async def analyze_plant(image: UploadFile = File(...), db: Session = Depends(get_db)):
    """Загружает изображение, анализирует его с помощью Gemini и сохраняет результат."""
    
    if not image:
        raise HTTPException(status_code=400, detail="Файл не загружен")

    image_data = await image.read()

    if not image_data:
        raise HTTPException(status_code=400, detail="Файл пустой")

    filename = f"plants/{image.filename}"
    image_url = upload_to_s3(image_data, filename)

    analysis_result = analyze_image_with_gemini(image_data, image.content_type)

    # Логируем, что возвращает Gemini
    logging.debug(f"🔍 Ответ от Gemini: {analysis_result}")

    if not isinstance(analysis_result, dict):
        raise HTTPException(status_code=500, detail="Некорректный формат ответа от Gemini")

    if "diagnosis" not in analysis_result or "recommendation" not in analysis_result:
        raise HTTPException(status_code=500, detail=f"Некорректный ответ от Gemini: {analysis_result}")

    save_analysis_result(db, image_url, analysis_result["diagnosis"], analysis_result["recommendation"])

    return {
        "status": "success",
        "image_url": image_url,
        "diagnosis": analysis_result["diagnosis"],
        "recommendation": analysis_result["recommendation"]
    }
