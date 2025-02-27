from sqlalchemy.orm import Session
from models.vision_analysis import VisionAnalysis
import logging

def save_analysis_result(db: Session, image_url: str, diagnosis: str, recommendation: str):
    """Сохраняет результат анализа в базе данных с обработкой ошибок."""
    try:
        new_entry = VisionAnalysis(
            image_url=image_url,
            diagnosis=diagnosis,
            recommendation=recommendation
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except Exception as e:
        db.rollback()
        logging.error(f"Ошибка сохранения в БД: {str(e)}")
        return None
