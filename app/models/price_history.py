# app/models/price_history.py
from typing import TYPE_CHECKING

from sqlalchemy import Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    price: Mapped[float] = mapped_column(Float)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    product: Mapped["Product"] = relationship("Product", back_populates="price_history")
