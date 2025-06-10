# app/api/exceptions.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "detail": "Validation error",
                    "errors": exc.errors()
                }
            },
        )
    # Если ошибка другого типа — возвращаем None, пусть обработает другой handler
    return JSONResponse(
        status_code=500,
        content={"error": {"detail": "Internal server error"}}
    )
