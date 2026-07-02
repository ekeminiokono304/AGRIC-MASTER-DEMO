import io
import base64

from app.core.groq_service import groq_service
from app.core.exceptions import PredictionError
from app.schemas.disease_schema import DiseaseResponse


def predict_disease(image_bytes: bytes) -> DiseaseResponse:
    try:
        # Convert image bytes to base64 for textual representation
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        image_description = f"Image data (base64): {image_b64[:100]}..."
        
        result = groq_service.predict_disease(image_description=image_description)
    except Exception as exc:
        raise PredictionError("disease", str(exc)) from exc

    return DiseaseResponse(
        disease_name=result["disease_name"],
        confidence=result["confidence"],
        severity_score=result["severity_score"],
        treatment_plan=result["treatment_plan"],
    )
