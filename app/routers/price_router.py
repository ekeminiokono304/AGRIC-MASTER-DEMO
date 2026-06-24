from fastapi import APIRouter

from app.schemas.price_schema import PriceRequest, PriceResponse
from app.services.price_service import forecast_price

router = APIRouter()


@router.post("", response_model=PriceResponse)
def get_price_forecast(payload: PriceRequest):
    return forecast_price(payload)
