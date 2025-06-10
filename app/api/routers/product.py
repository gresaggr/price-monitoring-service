# app/api/routers/product.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.database import get_db


router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.url == product.url))
    existing_product = result.scalars().first()

    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    # Заглушка для парсинга цены
    new_price = 999.99
    db_product = Product(url=product.url, name=product.name, current_price=new_price)

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    return db_product


@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.get("/", response_model=list[ProductResponse])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products


@router.post("/{product_id}/check-price")
async def trigger_check_price(product_id: int):
    from app.tasks.celery_tasks import check_product_price_task
    task = check_product_price_task.delay(product_id)
    return {"task_id": task.id, "status": "Task triggered"}