import numpy as np

from app.core.model_loader import model_manager
from app.core.exceptions import PredictionError
from app.schemas.price_schema import PriceRequest, PriceResponse, PriceForecastPoint

# Demo-level placeholder current prices (naira/kg) -- replace with a live feed if available.
BASE_PRICES = {"maize": 450.0, "rice": 620.0}


def forecast_price(payload: PriceRequest) -> PriceResponse:
    model = model_manager.get("price")

    try:
        horizon = np.arange(30).reshape(-1, 1)  # placeholder feature window -- match your training features
        predictions = model.predict(horizon)
        forecast = [
            PriceForecastPoint(day=i + 1, predicted_price=round(float(p), 2))
            for i, p in enumerate(predictions[:30])
        ]
    except Exception as exc:
        raise PredictionError("price", str(exc)) from exc

    return PriceResponse(
        commodity=payload.commodity,
        market=payload.market,
        current_price=BASE_PRICES.get(payload.commodity.lower(), 0.0),
        forecast=forecast,
    )
