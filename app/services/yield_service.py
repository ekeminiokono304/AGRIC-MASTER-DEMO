import numpy as np

from app.core.model_loader import model_manager
from app.core.exceptions import PredictionError
from app.schemas.yield_schema import YieldRequest, YieldResponse

CROP_ENCODING = {"maize": 0, "rice": 1, "cassava": 2, "yam": 3, "sorghum": 4}
SOIL_ENCODING = {"loamy": 0, "sandy": 1, "clay": 2, "silty": 3}


def predict_yield(payload: YieldRequest) -> YieldResponse:
    model = model_manager.get("yield")

    try:
        features = np.array([[
            CROP_ENCODING.get(payload.crop_type.lower(), 0),
            SOIL_ENCODING.get(payload.soil_type.lower(), 0),
            payload.rainfall_mm,
            payload.fertilizer_kg_per_ha,
            payload.farm_size_ha,
        ]])
        prediction = float(model.predict(features)[0])
        margin = prediction * 0.12  # demo-level confidence band
    except Exception as exc:
        raise PredictionError("yield", str(exc)) from exc

    return YieldResponse(
        predicted_yield_tons_per_ha=round(prediction, 2),
        confidence_interval_low=round(prediction - margin, 2),
        confidence_interval_high=round(prediction + margin, 2),
        region=payload.region,
        crop_type=payload.crop_type,
    )
