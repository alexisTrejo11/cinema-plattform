from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False
    SERVICE_NAME: str = "wallet-service"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_AUDIENCE: str | None = None
    JWT_ISSUER: str | None = None
    JWT_LEEWAY_SECONDS: Optional[int] = 300

    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 50055

    POSTGRES_VALIDATE_ON_STARTUP: bool = True
    REDIS_VALIDATE_ON_STARTUP: bool = True

    # ── Kafka (optional; publish wallet transaction events) ─────────────────
    KAFKA_ENABLED: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CLIENT_ID: str = "wallet-service"
    KAFKA_WALLET_EVENTS_TOPIC: str = "wallet.events"

    # ── Service registry (optional) ───────────────────────────────────────────
    REGISTRY_ENABLED: bool = False
    REGISTRY_ADMIN_URL: str = "http://localhost:8080"

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def postgres_db_url(self) -> str:
        return self.get_database_url()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
