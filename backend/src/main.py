import sentry_sdk
from fastapi import FastAPI
from src.core.config import settings


# Инициализация Sentry
if settings.is_sentry_enabled:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profile_lifecycle=1.0
    )

# Настройка FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for shop",
    version="0.1.0"
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

