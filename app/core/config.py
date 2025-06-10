# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    SECRET_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    CHECK_INTERVAL: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    print(f"Current working dir: {os.getcwd()}")
    settings = Settings()
    print("Loaded settings:", settings.model_dump())
    return settings
