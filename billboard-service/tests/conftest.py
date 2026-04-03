import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config.base_model import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def engine():
    # Import all models to ensure they are registered with SQLAlchemy
    from app.showtime.infrastructure.persistence.models import ShowtimeModel  # type: ignore
    from app.movies.infrastructure.persistence.models import MovieModel  # type: ignore
    from app.theater.infrastructure.persistence.models import TheaterModel, TheaterSeatModel  # type: ignore
    from app.cinema.infrastructure.persistence.cinema_model import CinemaModel  # type: ignore
    from app.showtime.infrastructure.persistence.models import ShowtimeSeatModel  # type: ignore

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
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
