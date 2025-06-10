# 🛒 Price Monitoring Service

Сервис для отслеживания цен на товары по URL.

## 🧩 Функционал

- Добавление товаров по URL
- Асинхронный парсинг цен
- Отслеживание изменений
- Хранение истории цен в PostgreSQL
- Уведомления через Celery + Redis

## 🛠️ Технологии

- **FastAPI** — асинхронный API
- **Celery + Redis** — фоновые задачи
- **PostgreSQL + SQLAlchemy** — ORM и хранение данных
- **Docker** — контейнеризация
- **BeautifulSoup + httpx** — парсинг страниц

## 🔐 Переменные окружения

Создайте `.env` из `example.env`.

## 🚀 Запуск

Под Windows в случае ошибок с портами:
```bash
net stop winnat
```

Применить миграции:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

Локальная разработка

```bash
docker-compose up --build
```