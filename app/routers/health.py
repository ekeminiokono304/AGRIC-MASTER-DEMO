from fastapi import APIRouter

from app.core.groq_service import groq_service

router = APIRouter()


@router.get("/health")
def health_check():
    """Quick pre-demo check: see at a glance if the Groq LLM API is live."""
    api_ready = bool(groq_service.api_key)
    return {
        "status": "ok",
        "models": {
            "groq_llm": "ready" if api_ready else "api_key_missing"
        },
        "all_models_ready": api_ready,
    }
