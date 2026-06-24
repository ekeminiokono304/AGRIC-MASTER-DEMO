from typing import List, Optional
from pydantic import BaseModel


class SensorReading(BaseModel):
    heart_rate: float
    temperature: float
    activity_level: float


class LivestockRequest(BaseModel):
    animal_id: str
    readings: List[SensorReading]


class LivestockResponse(BaseModel):
    animal_id: str
    is_anomaly: bool
    anomaly_score: float
    flagged_reading_index: Optional[int] = None
