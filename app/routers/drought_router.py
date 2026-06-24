from fastapi import APIRouter

from app.schemas.drought_schema import DroughtRequest, DroughtResponse
from app.services.drought_service import score_drought_risk

router = APIRouter()


@router.post("", response_model=DroughtResponse)
def get_drought_risk(payload: DroughtRequest):
    return score_drought_risk(payload)
