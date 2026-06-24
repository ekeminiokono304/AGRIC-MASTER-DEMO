from fastapi import APIRouter

from app.core.model_loader import model_manager

router = APIRouter()


@router.get("/health")
def health_check():
    """Quick pre-demo check: see at a glance which models are actually live."""
    statuses = model_manager.status_report()
    return {
        "status": "ok",
        "models": statuses,
        "all_models_ready": all(s == "loaded" for s in statuses.values()),
    }
