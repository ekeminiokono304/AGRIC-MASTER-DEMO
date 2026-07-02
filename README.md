# AGRIC-MASTER API

FastAPI backend serving 5 intelligent agriculture services for the AGRIC-MASTER investor demo: crop yield prediction, plant disease classification, commodity price forecasting, livestock anomaly detection, and drought risk scoring. 

The application utilizes **Groq's ultra-fast LPU inference API (LLaMA-3 70B)** acting as an agricultural expert, rather than relying on static, bulky traditional ML models.

## Architecture

```text
app/
├── main.py            # FastAPI entry point, CORS, exception handlers
├── core/
│   ├── config.py      # Pydantic settings (.env-driven)
│   ├── groq_service.py# Unified LLM-inference service powered by Groq
│   └── exceptions.py  # Custom exceptions -> clean JSON error responses
├── routers/           # HTTP layer only — one file per module, calls into services/
├── schemas/           # Pydantic request/response models
└── services/          # Business logic — preprocessing, LLM requests, postprocessing
```

Routers never touch inference logic directly — they call a service function, which interacts with `groq_service`. This modular architecture keeps each of the 5 modules independently testable and clean.

## Local setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You must configure your Groq API key in your `.env` file for the predictors to work:
```bash
# Create the environment file
cp .env.example .env
```
Inside `.env`, ensure you supply your key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

To run the application:
```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive Swagger docs, or `http://localhost:8000/` to test if the API is running.

## Endpoints

| Method | Path                | Purpose                              |
|--------|---------------------|---------------------------------------|
| GET    | /                   | Status of API                         |
| POST   | /predict/yield      | Crop yield + confidence interval      |
| POST   | /predict/disease    | Upload leaf image description -> disease ID |
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

**Render** (`render.yaml` included): Push to GitHub, connect the repo on Render, and it builds from the Dockerfile automatically. Because we use Groq API, the backend requires very minimal RAM/disk overhead! 

**Docker SDK**: Fully containerized and lightweight, deploys cleanly to any modern platform without huge ML `.pkl` model overhead.
