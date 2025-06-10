# app/tasks/celery_beat.py
from app.tasks.celery_app import celery_app

# Просто стартуем beat
if __name__ == "__main__":
    celery_app.start(["beat", "--loglevel=INFO"])