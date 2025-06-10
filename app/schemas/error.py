from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: str


class ErrorResponse(BaseModel):
    error: ErrorModel
