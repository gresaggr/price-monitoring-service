# app/tasks/celery_app.py
import os
from celery import Celery
from datetime import timedelta

# Создаём экземпляр Celery
celery_app = Celery("worker")
celery_app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

# Получаем интервал из .env
update_delta = int(os.getenv("CHECK_INTERVAL", "60"))

# Расписание для Beat
celery_app.conf.beat_schedule = {
    "check-all-products-periodically": {
        "task": "check_all_products_prices_task",
        "schedule": timedelta(seconds=update_delta),
    }
}

celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["app.tasks.celery_tasks"], force=True)
