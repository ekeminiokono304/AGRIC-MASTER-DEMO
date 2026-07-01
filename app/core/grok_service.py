import json
import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger("agric_master.grok_service")


class GrokService:
    """
    Unified service for all model predictions using Grok API.
    Replaces individual model files with a single LLM-based inference backend.
    """

    BASE_URL = "https://api.x.ai/v1"
    MODEL = "grok-beta"

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set. Grok predictions will fail.")

    def _call_grok(self, prompt: str) -> str:
        """
        Send a prompt to Grok and return the response text.
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.BASE_URL}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPError as e:
            logger.error("Grok API error: %s", e)
            raise RuntimeError(f"Grok API call failed: {e}") from e

    def predict_yield(self, crop_type: str, soil_type: str, rainfall_mm: float,
                     fertilizer_kg_per_ha: float, farm_size_ha: float, region: str) -> Dict[str, Any]:
        """
        Use Grok to predict crop yield based on agricultural parameters.
        """
        prompt = f"""You are an agricultural expert. Based on the following farm parameters, 
estimate the expected crop yield in tons per hectare.

Farm Parameters:
- Crop Type: {crop_type}
- Soil Type: {soil_type}
- Rainfall: {rainfall_mm} mm
- Fertilizer: {fertilizer_kg_per_ha} kg/ha
- Farm Size: {farm_size_ha} hectares
- Region: {region}

Provide a JSON response with this exact structure:
{{
  "predicted_yield_tons_per_ha": <number>,
  "confidence_interval_low": <number>,
  "confidence_interval_high": <number>,
  "reasoning": "<brief explanation>"
}}

Only respond with valid JSON, no additional text."""

        response_text = self._call_grok(prompt)
        try:
            result = json.loads(response_text)
            return {
                "predicted_yield_tons_per_ha": result.get("predicted_yield_tons_per_ha", 0.0),
                "confidence_interval_low": result.get("confidence_interval_low", 0.0),
                "confidence_interval_high": result.get("confidence_interval_high", 0.0),
                "region": region,
                "crop_type": crop_type,
                "reasoning": result.get("reasoning", ""),
            }
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Grok response: %s", response_text)
            raise ValueError(f"Invalid Grok response: {e}") from e

    def predict_disease(self, image_description: str) -> Dict[str, Any]:
        """
        Use Grok to identify plant disease from description.
        """
        prompt = f"""You are a plant pathologist. Based on the following description of a plant leaf or crop,
identify potential diseases and recommend treatment.

Image Description: {image_description}

Provide a JSON response with this exact structure:
{{
  "disease_name": "<disease name>",
  "confidence": <0.0-1.0>,
  "severity_score": <0-100>,
  "treatment_plan": "<treatment recommendation>"
}}

Only respond with valid JSON, no additional text."""

        response_text = self._call_grok(prompt)
        try:
            result = json.loads(response_text)
            return {
                "disease_name": result.get("disease_name", "Unknown"),
                "confidence": result.get("confidence", 0.0),
                "severity_score": result.get("severity_score", 0),
                "treatment_plan": result.get("treatment_plan", "Consult a local agricultural extension officer."),
            }
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Grok response: %s", response_text)
            raise ValueError(f"Invalid Grok response: {e}") from e

    def predict_price(self, crop_type: str, market_region: str, season: str, quality_grade: str) -> Dict[str, Any]:
        """
        Use Grok to estimate crop market price.
        """
        prompt = f"""You are an agricultural market analyst. Based on the following crop and market information,
estimate the current market price per kg.

Crop Information:
- Crop Type: {crop_type}
- Market Region: {market_region}
- Season: {season}
- Quality Grade: {quality_grade}

Provide a JSON response with this exact structure:
{{
  "estimated_price_per_kg": <number>,
  "price_range_low": <number>,
  "price_range_high": <number>,
  "market_analysis": "<brief market analysis>"
}}

Only respond with valid JSON, no additional text."""

        response_text = self._call_grok(prompt)
        try:
            result = json.loads(response_text)
            return {
                "estimated_price_per_kg": result.get("estimated_price_per_kg", 0.0),
                "price_range_low": result.get("price_range_low", 0.0),
                "price_range_high": result.get("price_range_high", 0.0),
                "currency": "USD",
                "market_analysis": result.get("market_analysis", ""),
            }
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Grok response: %s", response_text)
            raise ValueError(f"Invalid Grok response: {e}") from e

    def predict_livestock_health(self, animal_type: str, symptoms: str, age_months: int,
                                location: str) -> Dict[str, Any]:
        """
        Use Grok to assess livestock health status.
        """
        prompt = f"""You are a veterinary expert specializing in livestock. Based on the following information,
assess the animal's health status and recommend actions.

Animal Information:
- Type: {animal_type}
- Age: {age_months} months
- Symptoms: {symptoms}
- Location: {location}

Provide a JSON response with this exact structure:
{{
  "health_status": "<Healthy/At-Risk/Critical>",
  "risk_score": <0-100>,
  "recommended_actions": "<specific recommendations>",
  "estimated_intervention_cost": <number>
}}

Only respond with valid JSON, no additional text."""

        response_text = self._call_grok(prompt)
        try:
            result = json.loads(response_text)
            return {
                "health_status": result.get("health_status", "Unknown"),
                "risk_score": result.get("risk_score", 0),
                "recommended_actions": result.get("recommended_actions", "Consult a veterinarian"),
                "estimated_intervention_cost": result.get("estimated_intervention_cost", 0.0),
            }
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Grok response: %s", response_text)
            raise ValueError(f"Invalid Grok response: {e}") from e

    def predict_drought_risk(self, region: str, soil_moisture_percent: float,
                            rainfall_last_30_days_mm: float, temperature_avg_c: float) -> Dict[str, Any]:
        """
        Use Grok to assess drought risk for a region.
        """
        prompt = f"""You are a climate and agriculture specialist. Based on the following environmental data,
assess the drought risk for a region and recommend mitigation strategies.

Environmental Data:
- Region: {region}
- Soil Moisture: {soil_moisture_percent}%
- Rainfall (last 30 days): {rainfall_last_30_days_mm} mm
- Average Temperature: {temperature_avg_c}°C

Provide a JSON response with this exact structure:
{{
  "drought_risk_level": "<Low/Moderate/High/Severe>",
  "risk_score": <0-100>,
  "days_until_critical": <number or null>,
  "mitigation_strategies": "<recommended actions>"
}}

Only respond with valid JSON, no additional text."""

        response_text = self._call_grok(prompt)
        try:
            result = json.loads(response_text)
            return {
                "drought_risk_level": result.get("drought_risk_level", "Unknown"),
                "risk_score": result.get("risk_score", 0),
                "days_until_critical": result.get("days_until_critical"),
                "mitigation_strategies": result.get("mitigation_strategies", ""),
            }
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Grok response: %s", response_text)
            raise ValueError(f"Invalid Grok response: {e}") from e


grok_service = GrokService()
