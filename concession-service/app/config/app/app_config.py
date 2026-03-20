from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # Application Configuration
    API_NAME: str = "Product Service"
    API_HOST: str
    API_PORT: int
    API_VERSION: str = "2.0"
    DEBUG_MODE: bool = False

    REGISTRY_ADMIN_URL: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # Database Configuration
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"

    RABBITMQ_URL: str
    USER_EVENTS_EXCHANGE: str
    CONSUMER_QUEUE_NAME: str

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
