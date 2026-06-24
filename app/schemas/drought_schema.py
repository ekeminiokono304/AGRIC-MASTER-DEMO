from pydantic import BaseModel


class DroughtRequest(BaseModel):
    region: str
    rainfall_mm: float
    avg_temperature_c: float
    soil_moisture_pct: float


class DroughtResponse(BaseModel):
    region: str
    drought_risk_score: float
    risk_level: str
    outlook_90_day: str
