# Dockerfile
FROM python:3.11-slim

# Установка зависимостей ОС
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-login --gecos '' celeryuser

# Создаём рабочую папку и даём права пользователю
WORKDIR /app

# Даём пользователю celeryuser доступ к /app
RUN chown -R celeryuser:celeryuser /app

# Копируем только requirements.txt сначала — для кэширования установки pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Переключаемся на непривилегированного пользователя
USER celeryuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]