from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from services.gemini import analyze_image_with_gemini
from services.storage import upload_to_s3
from services.db_operations import save_analysis_result
from models.database import get_db
import logging

router = APIRouter()

@router.post("/analyze/")
async def analyze_plant(image: UploadFile = File(...), db: Session = Depends(get_db)):
    """Загружает изображение, анализирует его с помощью Gemini и сохраняет результат."""
    
    try:
        if not image:
            raise HTTPException(status_code=400, detail="Файл не загружен")

        image_data = await image.read()
        if not image_data:
            raise HTTPException(status_code=400, detail="Файл пустой")

        filename = f"plants/{image.filename}"
        image_url = upload_to_s3(image_data, filename)

        if not image_url:
            raise HTTPException(status_code=500, detail="Ошибка загрузки в AWS S3")

        analysis_result = analyze_image_with_gemini(image_data, image.content_type)

        if "error" in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result["message"])

        save_analysis_result(db, image_url, analysis_result["diagnosis"], analysis_result["recommendation"])

        return {
            "status": "success",
            "image_url": image_url,
            "diagnosis": analysis_result["diagnosis"],
            "recommendation": analysis_result["recommendation"]
        }
    
    except Exception as e:
        logging.error(f"Ошибка обработки изображения: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка обработки изображения")
