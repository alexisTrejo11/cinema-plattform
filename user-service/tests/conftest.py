import asyncio
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

os.environ.setdefault("POSTGRES_VALIDATE_ON_STARTUP", "false")
os.environ.setdefault("REDIS_VALIDATE_ON_STARTUP", "false")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "cinema_users_test")
os.environ.setdefault("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")

from app.config.postgres_config import Base
import sqlite3


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def engine():

    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"detect_types": sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
