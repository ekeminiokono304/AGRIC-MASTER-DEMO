from pydantic import BaseModel, Field


class YieldRequest(BaseModel):
    region: str = Field(..., examples=["Akwa Ibom"])
    crop_type: str = Field(..., examples=["maize"])
    soil_type: str = Field(..., examples=["loamy"])
    rainfall_mm: float = Field(..., examples=[850.0])
    fertilizer_kg_per_ha: float = Field(..., examples=[120.0])
    farm_size_ha: float = Field(..., examples=[2.5])


class YieldResponse(BaseModel):
    predicted_yield_tons_per_ha: float
    confidence_interval_low: float
    confidence_interval_high: float
    region: str
    crop_type: str
