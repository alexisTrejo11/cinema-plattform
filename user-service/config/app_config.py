from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    rabbitmq_url: str 
    
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