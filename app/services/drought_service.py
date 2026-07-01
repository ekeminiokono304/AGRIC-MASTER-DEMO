from app.core.grok_service import grok_service
from app.core.exceptions import PredictionError
from app.schemas.drought_schema import DroughtRequest, DroughtResponse


_RISK_LEVEL_MAP = {
    "Low": 0.2,
    "Moderate": 0.5,
    "High": 0.75,
    "Severe": 0.95,
}

_OUTLOOKS = {
    "Low": "Conditions expected to remain stable over the next 90 days.",
    "Moderate": "Some dry spells possible; monitor rainfall trends closely.",
    "High": "Elevated drought risk; consider water conservation measures now.",
    "Severe": "Critical drought risk; immediate irrigation and contingency planning advised.",
}


def score_drought_risk(payload: DroughtRequest) -> DroughtResponse:
    try:
        result = grok_service.predict_drought_risk(
            region=payload.region,
            soil_moisture_percent=payload.soil_moisture_pct,
            rainfall_last_30_days_mm=payload.rainfall_mm,
            temperature_avg_c=payload.avg_temperature_c,
        )
        
        level = result["drought_risk_level"]
        score = _RISK_LEVEL_MAP.get(level, 0.5)
        
    except Exception as exc:
        raise PredictionError("drought", str(exc)) from exc

    return DroughtResponse(
        region=payload.region,
        drought_risk_score=round(score, 3),
        risk_level=level,
        outlook_90_day=_OUTLOOKS.get(level, "Unable to determine outlook."),
    )
