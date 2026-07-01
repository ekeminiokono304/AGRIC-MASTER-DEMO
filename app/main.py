import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import PredictionError
from app.routers import disease_router, drought_router, health, livestock_router, price_router, yield_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    return JSONResponse(
        status_code=500,
        content={"error": "prediction_failed", "model": exc.model_name, "detail": exc.detail},
    )


app.include_router(health.router, tags=["health"])
app.include_router(yield_router.router, prefix="/predict/yield", tags=["yield"])
app.include_router(disease_router.router, prefix="/predict/disease", tags=["disease"])
app.include_router(price_router.router, prefix="/predict/price", tags=["price"])
app.include_router(livestock_router.router, prefix="/predict/livestock", tags=["livestock"])
app.include_router(drought_router.router, prefix="/predict/drought", tags=["drought"])


@app.get("/")
def root():
    return {"message": "AGRIC-MASTER API is running", "docs": "/docs"}
