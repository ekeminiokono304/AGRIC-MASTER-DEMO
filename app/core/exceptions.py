class ModelNotLoadedException(Exception):
    """Raised when a router asks for a model that isn't loaded/available."""

    def __init__(self, model_name: str, status: str):
        self.model_name = model_name
        self.status = status
        super().__init__(f"Model '{model_name}' is not available (status: {status})")


class PredictionError(Exception):
    """Raised when a model loaded fine but failed during inference."""

    def __init__(self, model_name: str, detail: str):
        self.model_name = model_name
        self.detail = detail
        super().__init__(f"Prediction failed for '{model_name}': {detail}")
