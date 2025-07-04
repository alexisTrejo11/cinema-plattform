from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file="./.env",       
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    app_name: str = "CINEMA API: Ticket Service"
    app_version: str = "2.0.0"
    app_port: Optional[int] = None
    app_debug: bool = True
    app_summary: str = "Microservice that manages tickets operation for showtimes"
    
    atlas_uri : str
    postgres_uri: str
    mongo_db_name: Optional[str] = None
    
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 3600


settings = Settings() # type: ignore
