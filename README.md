# AGRIC-MASTER API

FastAPI backend serving 5 trained ML models for the AGRIC-MASTER investor demo:
crop yield prediction, plant disease classification, commodity price
forecasting, livestock anomaly detection, and drought risk scoring.

## Architecture

```
app/
├── main.py            # FastAPI entry point, CORS, exception handlers, startup model loading
├── core/
│   ├── config.py      # Pydantic settings (.env-driven)
│   ├── model_loader.py# Singleton ModelManager — graceful failure if a model is missing/broken
│   └── exceptions.py  # Custom exceptions -> clean JSON error responses
├── routers/           # HTTP layer only — one file per module, calls into services/
├── schemas/           # Pydantic request/response models
└── services/          # Business logic — preprocessing, inference, postprocessing
models/                # Trained model files go here (see models/README.md)
```

Routers never touch model internals directly — they call a service function,
which calls `model_manager.get(name)`. This keeps each of the 5 modules
independently testable and means a broken model degrades gracefully instead
of crashing the whole API mid-demo.

## Local setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # fill in real API keys if you use them
```

Drop your trained model files into `models/` (see `models/README.md` for
exact filenames), then run:

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive Swagger docs, or
`http://localhost:8000/health` to see which models are currently loaded.

## Training workflow

Train in Colab (free GPU) → export to `.pkl` (joblib) or `.pt` (torch) →
drop the file into `models/` with the exact name from `models/README.md` →
restart the API. No code changes needed.

## Endpoints

| Method | Path                | Purpose                              |
|--------|---------------------|---------------------------------------|
| GET    | /health             | Status of all 5 models                |
| POST   | /predict/yield      | Crop yield + confidence interval      |
| POST   | /predict/disease    | Upload leaf image -> disease ID       |
| POST   | /predict/price      | 30-day commodity price forecast       |
| POST   | /predict/livestock  | Sensor readings -> anomaly flag       |
| POST   | /predict/drought    | Drought risk score + 90-day outlook   |

Example:

```bash
curl -X POST http://localhost:8000/predict/yield \
  -H "Content-Type: application/json" \
  -d '{"region":"Akwa Ibom","crop_type":"maize","soil_type":"loamy","rainfall_mm":850,"fertilizer_kg_per_ha":120,"farm_size_ha":2.5}'
```

## Deployment notes

**Render** (`render.yaml` included): push to GitHub, connect the repo on
Render, it builds from the Dockerfile automatically. Free tier has limited
RAM/disk — fine for the 4 scikit-learn models, but watch the disease model.

**Hugging Face Spaces (Docker SDK)**: better fit if `disease_model.pt` (or
any model file) exceeds ~50MB, since GitHub blocks large file pushes by
default. HF Spaces free tier gives 16GB RAM / 50GB storage and runs the same
Dockerfile with no code changes — just set the Space's port to read `$PORT`
(already handled in the Dockerfile here).

**Before any live demo**: hit `/health` first. If `all_models_ready` is
`false`, you'll know exactly which module to avoid clicking on stage, instead
of finding out live.
