import logging
import os
from enum import Enum
from typing import Any, Dict, Optional

import joblib

logger = logging.getLogger("agric_master.model_loader")


class ModelStatus(str, Enum):
    LOADED = "loaded"
    UNAVAILABLE = "unavailable"
    NOT_FOUND = "not_found"


# filename + how to load it. Add new models here only -- nothing else changes.
MODEL_REGISTRY = {
    "yield": ("yield_model.pkl", "joblib"),
    "disease": ("disease_model.pt", "torch"),
    "price": ("price_model.pkl", "joblib"),
    "livestock": ("livestock_model.pkl", "joblib"),
    "drought": ("drought_model.pkl", "joblib"),
}


class ModelManager:
    """
    Singleton model manager with graceful failure.

    Loads every registered model once at startup. If one model file is
    missing or corrupted, that single model is marked UNAVAILABLE/NOT_FOUND
    and the app keeps running -- one broken model must never take down the
    whole demo. Routers ask for a model via .get(name) and get a clean,
    catchable exception if it isn't ready, instead of a server crash.
    """

    _instance: Optional["ModelManager"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models: Dict[str, Any] = {}
            cls._instance._status: Dict[str, ModelStatus] = {}
        return cls._instance

    def load_all(self, model_dir: str) -> None:
        for name, (filename, loader_type) in MODEL_REGISTRY.items():
            path = os.path.join(model_dir, filename)

            if not os.path.exists(path):
                logger.warning("Model file not found: %s (%s)", name, path)
                self._status[name] = ModelStatus.NOT_FOUND
                continue

            try:
                if loader_type == "joblib":
                    self._models[name] = joblib.load(path)
                elif loader_type == "torch":
                    import torch  # lazy import -- only pulled in if a .pt model actually exists

                    loaded = torch.load(path, map_location="cpu")
                    if hasattr(loaded, "eval"):
                        loaded.eval()
                    self._models[name] = loaded
                else:
                    raise ValueError(f"Unknown loader_type '{loader_type}' for model '{name}'")

                self._status[name] = ModelStatus.LOADED
                logger.info("Model loaded: %s", name)
            except Exception as exc:  # noqa: BLE001 -- intentional: one bad model must not crash startup
                logger.error("Failed to load model '%s': %s", name, exc)
                self._status[name] = ModelStatus.UNAVAILABLE

    def get(self, name: str) -> Any:
        from app.core.exceptions import ModelNotLoadedException

        if self._status.get(name) != ModelStatus.LOADED:
            raise ModelNotLoadedException(name, self._status.get(name, ModelStatus.NOT_FOUND))
        return self._models[name]

    def status_report(self) -> Dict[str, str]:
        return {name: self._status.get(name, ModelStatus.NOT_FOUND).value for name in MODEL_REGISTRY}


model_manager = ModelManager()
