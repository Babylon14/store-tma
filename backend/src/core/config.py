from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Настройки приложения """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- FASTAPI PROJECT INFO ---
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- DATABASE ---
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str  # Будет использоваться для SQLAlchemy

    # --- REDIS & CELERY ---
    REDIS_URL: RedisDsn
    
    # --- SENTRY ---
    SENTRY_DSN: str | None = None
    
    # --- TELEGRAM ---
    BOT_TOKEN: str
    PAYMENT_PROVIDER_TOKEN: str | None = None
    MANAGER_ID: int
    
    
    @property
    def is_sentry_enabled(self) -> bool:
        """ Возвращает True если SENTRY_DSN не пустой и не "your_sentry_dsn_here" """
        return bool(self.SENTRY_DSN and self.SENTRY_DSN != "your_sentry_dsn_here")


settings = Settings()

