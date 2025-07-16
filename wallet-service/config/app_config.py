from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

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
