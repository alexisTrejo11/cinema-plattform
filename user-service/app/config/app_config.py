from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: Optional[str] = None
    JWT_ISSUER: Optional[str] = None
    JWT_LEEWAY_SECONDS: int = 0

    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 50051

    # Fail-fast startup check for DB connectivity and schema.
    POSTGRES_VALIDATE_ON_STARTUP: bool = True

    # Fail-fast startup check for Redis (ping + short read/write probe).
    REDIS_VALIDATE_ON_STARTUP: bool = True

    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", extra="ignore"
    )

    def postgres_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


@lru_cache()
def get_settings_cached_instance():
    """
    Returns a cached instance of the Settings.
    This ensures the .env file is read only once.
    """
    return Settings()


settings = get_settings_cached_instance()
