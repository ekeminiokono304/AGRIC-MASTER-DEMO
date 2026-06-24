import numpy as np

from app.core.model_loader import model_manager
from app.core.exceptions import PredictionError
from app.schemas.drought_schema import DroughtRequest, DroughtResponse


def _risk_level(score: float) -> str:
    if score < 0.3:
        return "Low"
    if score < 0.6:
        return "Moderate"
    if score < 0.8:
        return "High"
    return "Severe"


_OUTLOOKS = {
    "Low": "Conditions expected to remain stable over the next 90 days.",
    "Moderate": "Some dry spells possible; monitor rainfall trends closely.",
    "High": "Elevated drought risk; consider water conservation measures now.",
    "Severe": "Critical drought risk; immediate irrigation and contingency planning advised.",
}


def score_drought_risk(payload: DroughtRequest) -> DroughtResponse:
    model = model_manager.get("drought")

    try:
        features = np.array([[payload.rainfall_mm, payload.avg_temperature_c, payload.soil_moisture_pct]])
        score = max(0.0, min(1.0, float(model.predict(features)[0])))
    except Exception as exc:
        raise PredictionError("drought", str(exc)) from exc

    level = _risk_level(score)
    return DroughtResponse(
        region=payload.region,
        drought_risk_score=round(score, 3),
        risk_level=level,
        outlook_90_day=_OUTLOOKS[level],
    )
