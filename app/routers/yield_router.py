from fastapi import APIRouter

from app.schemas.yield_schema import YieldRequest, YieldResponse
from app.services.yield_service import predict_yield

router = APIRouter()


@router.post("", response_model=YieldResponse)
def get_yield_prediction(payload: YieldRequest):
    return predict_yield(payload)
