# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости (без создания venv внутри контейнера для простоты)
RUN uv pip install --system --no-cache -r pyproject.toml

# Копируем исходный код
COPY . .

# Переменная окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Команда запуска будет переопределена в docker-compose

