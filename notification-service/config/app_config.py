from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from twilio.rest import Client as TwilioClient


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "CINEMA API: Notification Service"
    app_version: str = "2.0.0"
    app_port: Optional[int] = None
    app_debug: bool = True
    app_summary: str = "Microservice that manages notification operation for the system"

    atlas_uri: str
    mongo_db_name: Optional[str] = None

    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 3600

    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str
    smtp_password: str
    from_email: str
    from_name: str = "Cinema App"

    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str


settings = Settings()  # type: ignore


class EmailConfig:
    smtp_server: str = settings.smtp_server
    smtp_port: int = settings.smtp_port
    smtp_username: str = settings.smtp_username
    smtp_password: str = settings.smtp_password
    from_email: str = settings.from_email
    from_name: str = settings.from_name


twilio_client = TwilioClient(settings.twilio_auth_token, settings.twilio_auth_token)
