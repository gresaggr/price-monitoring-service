# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import get_settings
from app.api.routers.product import router as product_router
from app.api.exceptions import validation_exception_handler

settings = get_settings()

app = FastAPI(title="Price Monitoring Service")

# Регистрация обработчика ошибок
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключаем маршруты
app.include_router(product_router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "environment": {
            "DATABASE_URL": settings.DATABASE_URL,
            "CELERY_BROKER_URL": settings.CELERY_BROKER_URL,
            "POSTGRES_USER": settings.POSTGRES_USER,
            "POSTGRES_DB": settings.POSTGRES_DB,
        }
    }
