# app/tasks/celery_tasks.py
import asyncio
import logging
import os

from celery import Celery
from sqlalchemy.future import select

from app.database import get_db
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.utils.parser import get_price_from_url

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Celery
celery_app = Celery("worker")
celery_app.config_from_object("app.tasks.celery_app")
celery_app.autodiscover_tasks(["app.tasks.celery_tasks"], force=True)


# --- Задачи ---
@celery_app.task(name="check_product_price_task")
def check_product_price_task(product_id: int):
    logger.info(f"🟦 Воркер PID_[{os.getpid()}] получил товар ID {product_id}")
    run_async(async_check_product_price(product_id))


async def async_check_product_price(product_id: int):
    logger.info(f"🟩 Проверяем товар ID {product_id}")
    async for db in get_db():
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            logger.warning(f"🔴 Товар с ID {product_id} не найден")
            return {"status": "error", "message": "Product not found"}

        new_price = await get_price_from_url(product.url)

        if new_price is None:
            logger.error(f"❌ Не удалось получить цену для товара ID {product_id}")
            return {"status": "error", "message": "Failed to parse price"}

        if new_price != product.current_price:
            logger.info(f"🟨 Цена изменена для товара {product.url}: {product.current_price} → {new_price}")

            product.current_price = new_price
            db.add(product)

            price_history = PriceHistory(
                product_id=product.id,
                price=new_price
            )
            db.add(price_history)

            await db.commit()
            return {"status": "updated", "old_price": product.current_price, "new_price": new_price}

        logger.info(f"🔵 Цена не изменилась для товара {product.url}: {new_price}")
        return {"status": "no_change", "price": new_price}


@celery_app.task(name="check_all_products_prices_task")
def check_all_products_prices_task():
    logger.info("🟢 Начинаем проверку всех товаров")
    run_async(async_check_all_products_prices_inner())


async def async_check_all_products_prices_inner():
    logger.info("🟩 async_check_all_products_prices_inner: Запущен")
    async for db in get_db():
        result = await db.execute(select(Product.id))
        product_ids = result.scalars().all()

        logger.info(f"Найдено {len(product_ids)} товаров")

        if not product_ids:
            logger.warning("🟡 Нет товаров для проверки")
            return {"status": "ok", "count": 0}

        for product_id in product_ids:
            logger.info(f"🟠 Отправляем задачу для товара ID {product_id}")
            check_product_price_task.delay(product_id)

        logger.info(f"🟢 Все задачи отправлены. Всего: {len(product_ids)}")
        return {"status": "ok", "total_checked": len(product_ids), "tasks_sent": len(product_ids)}


def run_async(coro):
    """Безопасный запуск асинхронного кода в синхронной задаче"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
