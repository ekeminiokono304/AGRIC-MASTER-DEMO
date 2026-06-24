from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AGRIC-MASTER API"
    MODEL_DIR: str = "models"
    ALLOWED_ORIGINS: List[str] = ["*"]

    GROQ_API_KEY: str = ""
    WEATHER_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
