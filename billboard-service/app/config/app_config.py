from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cinema Backend: Billboard Service API"
    app_version: str = "1.0.0"
    redis_url: str

    database_url: Optional[str] = None
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "cinema_billboard"
    db_echo: bool = False

    jwt_secret_key: str = ""
    jwt_algorithms: str = "HS256"
    jwt_audience: Optional[str] = None
    jwt_issuer: Optional[str] = None
    jwt_leeway_seconds: int = 0

    # Application behaviour
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            "postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def jwt_algorithms_list(self) -> list[str]:
        return [alg.strip() for alg in self.jwt_algorithms.split(",") if alg.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
