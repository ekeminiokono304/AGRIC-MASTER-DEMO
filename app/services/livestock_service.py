import numpy as np

from app.core.model_loader import model_manager
from app.core.exceptions import PredictionError
from app.schemas.livestock_schema import LivestockRequest, LivestockResponse


def detect_anomaly(payload: LivestockRequest) -> LivestockResponse:
    model = model_manager.get("livestock")

    try:
        features = np.array([[r.heart_rate, r.temperature, r.activity_level] for r in payload.readings])

        # IsolationForest convention: predict() gives -1 for anomaly, 1 for normal
        predictions = model.predict(features)
        scores = model.decision_function(features) if hasattr(model, "decision_function") else model.score_samples(features)

        anomaly_indices = [i for i, p in enumerate(predictions) if p == -1]
        is_anomaly = len(anomaly_indices) > 0
        anomaly_score = float(min(scores)) if is_anomaly else float(max(scores))
    except Exception as exc:
        raise PredictionError("livestock", str(exc)) from exc

    return LivestockResponse(
        animal_id=payload.animal_id,
        is_anomaly=is_anomaly,
        anomaly_score=round(anomaly_score, 3),
        flagged_reading_index=anomaly_indices[0] if is_anomaly else None,
    )
