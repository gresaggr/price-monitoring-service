# app/schemas/product.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    url: str


class ProductCreate(ProductBase):
    name: Optional[str] = None


class ProductUpdate(ProductBase):
    url: Optional[str] = None
    name: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    url: str
    name: Optional[str]
    current_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductHistoryResponse(BaseModel):
    checked_at: datetime
    price: float

    class Config:
        from_attributes = True
