from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_VERSION: str = "2.0.0"
    API_NAME: str = "notification-service"
    SERVICE_NAME: str = "notification-service"
    DEBUG_MODE: bool = False

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "notification_db"

    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_VALIDATE_ON_STARTUP: bool = False

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str | None = None
    JWT_ISSUER: str | None = None
    JWT_LEEWAY_SECONDS: int = 300

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    EMAIL_FROM_ADDRESS: str = "no-reply@cinema.local"
    EMAIL_FROM_NAME: str = "Cinema Platform"

    TWILIO_ENABLED: bool = False
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    KAFKA_ENABLED: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CLIENT_ID: str = "notification-service"
    KAFKA_TOPIC_NOTIFICATION_INCOMING: str = "notification.incoming"
    KAFKA_TOPIC_NOTIFICATION_EVENTS: str = "notification.events"
    KAFKA_TOPIC_NOTIFICATION_DLQ: str = "notification.dlq"

    KAFKA_CONSUMER_ENABLED: bool = False
    KAFKA_CONSUMER_GROUP_NOTIFICATION: str = "notification-service-consumer"
    KAFKA_CONSUMER_AUTO_OFFSET_RESET: str = "latest"
    KAFKA_CONSUMER_POLL_TIMEOUT_MS: int = 1000
    KAFKA_CONSUMER_TOPICS: str = "notification.incoming,cinema.user-service.events,wallet.events"

    USER_DIRECTORY_LOOKUP_ENABLED: bool = False
    USER_DIRECTORY_BASE_URL: str = "http://localhost:8001"
    USER_DIRECTORY_TIMEOUT_SECONDS: float = 3.0

    REGISTRY_ENABLED: bool = False
    REGISTRY_ADMIN_URL: str = "http://localhost:8080"

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
