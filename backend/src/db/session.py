""" Настройка асинхронного движка и фабрики сессий"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import settings


# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # Выводит SQL запросы в консоль
    future=True
)

# Создаем фабрику сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency для FastAPI
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            
            