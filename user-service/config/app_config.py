from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    model_config = SettingsConfigDict(
        env_file="./.env",       
        env_file_encoding='utf-8',
        extra='ignore'
    )

@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings.
    This ensures the .env file is read only once.
    """
    return Settings()