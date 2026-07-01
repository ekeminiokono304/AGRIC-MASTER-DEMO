from app.core.grok_service import grok_service
from app.core.exceptions import PredictionError
from app.schemas.livestock_schema import LivestockRequest, LivestockResponse


def detect_anomaly(payload: LivestockRequest) -> LivestockResponse:
    try:
        # Build symptoms string from readings
        readings_summary = "; ".join([
            f"Reading {i+1}: HR={r.heart_rate}, Temp={r.temperature}°C, Activity={r.activity_level}"
            for i, r in enumerate(payload.readings)
        ])
        
        result = grok_service.predict_livestock_health(
            animal_type=payload.animal_id.split("_")[0] if "_" in payload.animal_id else "cattle",
            symptoms=readings_summary,
            age_months=24,  # placeholder
            location="farm",  # placeholder
        )
        
        # Map health status to anomaly detection
        is_anomaly = result["health_status"] in ["At-Risk", "Critical"]
        anomaly_score = result["risk_score"] / 100.0
        
    except Exception as exc:
        raise PredictionError("livestock", str(exc)) from exc

    return LivestockResponse(
        animal_id=payload.animal_id,
        is_anomaly=is_anomaly,
        anomaly_score=round(anomaly_score, 3),
        flagged_reading_index=0 if is_anomaly else None,
    )
