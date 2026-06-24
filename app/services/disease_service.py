import io

from app.core.model_loader import model_manager
from app.core.exceptions import PredictionError
from app.schemas.disease_schema import DiseaseResponse

# Extend this to your full trained class list (e.g. 38 classes from PlantVillage).
CLASS_NAMES = [
    "Healthy", "Early Blight", "Late Blight", "Leaf Spot",
    "Bacterial Wilt", "Mosaic Virus", "Rust", "Powdery Mildew",
]

TREATMENT_PLANS = {
    "Healthy": "No action needed. Continue regular monitoring.",
    "Early Blight": "Apply copper-based fungicide; remove affected lower leaves.",
    "Late Blight": "Apply fungicide immediately; improve field drainage and airflow.",
    "Leaf Spot": "Remove infected leaves; rotate crops next season.",
    "Bacterial Wilt": "Remove and destroy infected plants; disinfect tools between use.",
    "Mosaic Virus": "Remove infected plants; control aphid populations.",
    "Rust": "Apply fungicide; avoid overhead watering.",
    "Powdery Mildew": "Apply sulfur-based fungicide; increase plant spacing.",
}


def _build_transform():
    # torchvision is imported lazily here -- it's only needed at the moment
    # a disease prediction actually runs, so deployments without this model
    # loaded yet stay lighter.
    from torchvision import transforms

    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


def predict_disease(image_bytes: bytes) -> DiseaseResponse:
    import torch
    from PIL import Image

    model = model_manager.get("disease")

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = _build_transform()(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            confidence, predicted_idx = torch.max(probabilities, dim=0)

        idx = int(predicted_idx.item())
        disease_name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else "Unknown"
        severity = round(float(confidence.item()) * 100, 1) if disease_name != "Healthy" else 0.0
    except Exception as exc:
        raise PredictionError("disease", str(exc)) from exc

    return DiseaseResponse(
        disease_name=disease_name,
        confidence=round(float(confidence.item()), 3),
        severity_score=severity,
        treatment_plan=TREATMENT_PLANS.get(disease_name, "Consult a local agricultural extension officer."),
    )
