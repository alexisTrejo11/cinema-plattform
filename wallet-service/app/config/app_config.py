from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Application Configuration
    API_NAME: str = "Wallet Service"
    API_HOST: str
    API_PORT: int
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False

    REGISTRY_ADMIN_URL: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_AUDIENCE: Optional[str] = None
    JWT_ISSUER: Optional[str] = None
    JWT_LEEWAY_SECONDS: int = 60

    # Database Configuration
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # RabbitMQ Configuration
    RABBITMQ_URL: str
    USER_EVENTS_EXCHANGE: str
    CONSUMER_QUEUE_NAME: str
    WALLET_EXCHANGE: str

    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings_cached_instance():
    """
    Returns a cached instance of the Settings.
    This ensures the .env file is read only once.
    """
    return Settings()  # type: ignore


settings = get_settings_cached_instance()
