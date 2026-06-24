from typing import List
from pydantic import BaseModel


class PriceForecastPoint(BaseModel):
    day: int
    predicted_price: float


class PriceRequest(BaseModel):
    commodity: str = "maize"
    market: str = "Lagos"


class PriceResponse(BaseModel):
    commodity: str
    market: str
    current_price: float
    forecast: List[PriceForecastPoint]
