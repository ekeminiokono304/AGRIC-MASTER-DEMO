from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.disease_schema import DiseaseResponse
from app.services.disease_service import predict_disease

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg"}


@router.post("", response_model=DiseaseResponse)
async def classify_disease(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Upload a JPEG or PNG leaf image.")

    image_bytes = await file.read()
    return predict_disease(image_bytes)
