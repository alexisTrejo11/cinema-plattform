import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config.postgres_config import Base
from app.wallet.infrastructure.persistence.sql.sqlalchemy_models import WalletSQLModel


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:root@localhost:5432/test-cinema-wallets"
)


@pytest_asyncio.fixture(scope="function")
async def engine():

    engine = create_async_engine(TEST_DATABASE_URL, echo=False, connect_args={})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
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
