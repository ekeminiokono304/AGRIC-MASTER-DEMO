from app.core.grok_service import grok_service
from app.core.exceptions import PredictionError
from app.schemas.price_schema import PriceRequest, PriceResponse, PriceForecastPoint


def forecast_price(payload: PriceRequest) -> PriceResponse:
    try:
        result = grok_service.predict_price(
            crop_type=payload.commodity,
            market_region=payload.market,
            season="current",
            quality_grade="standard",
        )
        
        # Generate forecast points from Grok's estimated price
        estimated_price = result["estimated_price_per_kg"]
        forecast = [
            PriceForecastPoint(day=i + 1, predicted_price=round(estimated_price * (1 - 0.01 * i), 2))
            for i in range(30)
        ]
    except Exception as exc:
        raise PredictionError("price", str(exc)) from exc

    return PriceResponse(
        commodity=payload.commodity,
        market=payload.market,
        current_price=result["estimated_price_per_kg"],
        forecast=forecast,
    )
