import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("🟩 Worker стартовал")
    celery_app.start(["worker", "--loglevel=INFO", "--concurrency=1"])
