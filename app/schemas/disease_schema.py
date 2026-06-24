from pydantic import BaseModel


class DiseaseResponse(BaseModel):
    disease_name: str
    confidence: float
    severity_score: float
    treatment_plan: str
