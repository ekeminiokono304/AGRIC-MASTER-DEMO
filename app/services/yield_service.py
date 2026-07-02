from app.core.groq_service import groq_service
from app.core.exceptions import PredictionError
from app.schemas.yield_schema import YieldRequest, YieldResponse


def predict_yield(payload: YieldRequest) -> YieldResponse:
    try:
        result = groq_service.predict_yield(
            crop_type=payload.crop_type,
            soil_type=payload.soil_type,
            rainfall_mm=payload.rainfall_mm,
            fertilizer_kg_per_ha=payload.fertilizer_kg_per_ha,
            farm_size_ha=payload.farm_size_ha,
            region=payload.region,
        )
    except Exception as exc:
        raise PredictionError("yield", str(exc)) from exc

    return YieldResponse(
        predicted_yield_tons_per_ha=result["predicted_yield_tons_per_ha"],
        confidence_interval_low=result["confidence_interval_low"],
        confidence_interval_high=result["confidence_interval_high"],
        region=payload.region,
        crop_type=payload.crop_type,
    )
