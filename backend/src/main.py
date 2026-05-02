import sentry_sdk
from fastapi import FastAPI

from src.core.config import settings
from src.api.v1.endpoints.categories_api import router as category_router


# Инициализация Sentry
if settings.is_sentry_enabled:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profile_lifecycle=1.0
    )

# Описываем метаданные тегов
tags_metadata = [
    {
        "name": "Categories",
        "description": "Операции для управления категориями товаров",
        "x-displayName": "Категории товаров",  
    },
]

# Настройка FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for shop",
    version="0.1.0",
    openapi_tags=tags_metadata,
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs"
    }
    

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0
#     return division_by_zero


# Подключаем роутер с префиксом
app.include_router(router=category_router, prefix="/api/v1/categories", tags=["Categories"])


