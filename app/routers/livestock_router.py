from fastapi import APIRouter

from app.schemas.livestock_schema import LivestockRequest, LivestockResponse
from app.services.livestock_service import detect_anomaly

router = APIRouter()


@router.post("", response_model=LivestockResponse)
def check_livestock_health(payload: LivestockRequest):
    return detect_anomaly(payload)
