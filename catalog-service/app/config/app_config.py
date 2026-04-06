from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_VERSION: str = "2.0.0"
    DEBUG_MODE: bool = False
    SERVICE_NAME: str = "catalog-service"

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
    # Inbound gRPC server bind.
    GRPC_TIMEOUT_SECONDS: float = 10.0

    # Optional full sync URL for Alembic (psycopg2). If unset, built from POSTGRES_*.
    ALEMBIC_DATABASE_URL: str | None = None

    POSTGRES_VALIDATE_ON_STARTUP: bool = True
    REDIS_VALIDATE_ON_STARTUP: bool = True

    # ── Kafka (optional producers; inbound consumers gated separately) ───────
    KAFKA_ENABLED: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CLIENT_ID: str = "ticket-service"

    # Topics (see docs/kafka-topics.md)
    KAFKA_TOPIC_BILLBOARD_EVENTS: str = "billboard.events"
    KAFKA_WALLET_EVENTS_TOPIC: str = "wallet.events"
    KAFKA_TOPIC_BILLBOARD_DLQ: str = "billboard.events.dlq"
    KAFKA_TOPIC_WALLET_DLQ: str = "wallet.events.dlq"
    KAFKA_TOPIC_PAYMENT_EVENTS: str = "payment.events"
    KAFKA_TOPIC_PAYMENT_INCOMING: str = "payment.incoming"

    # Consumers (ticket-service read-model sync; implement handlers separately)
    KAFKA_CONSUMER_ENABLED: bool = False
    KAFKA_CONSUMER_GROUP_BILLBOARD: str = "ticket-service-billboard"
    KAFKA_CONSUMER_GROUP_WALLET: str = "ticket-service-wallet"
    KAFKA_CONSUMER_GROUP_PAYMENT: str = "payment-service-consumer"
    KAFKA_CONSUMER_AUTO_OFFSET_RESET: str = "latest"
    KAFKA_CONSUMER_POLL_TIMEOUT_MS: int = 1000
    KAFKA_CONSUMER_BILLBOARD_ENABLED: bool = True
    KAFKA_CONSUMER_WALLET_ENABLED: bool = True
    KAFKA_CONSUMER_PAYMENT_ENABLED: bool = True

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

    def get_sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def postgres_db_url(self) -> str:
        return self.get_database_url()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
