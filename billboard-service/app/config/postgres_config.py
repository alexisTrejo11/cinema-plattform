from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config.app_config import settings
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = settings.resolved_database_url

engine = create_async_engine(DATABASE_URL, echo=settings.db_echo, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def verify_db_connection() -> None:
    """Fail fast during startup if the DB is not reachable."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            logger.info("Database connection check passed.")
    except SQLAlchemyError as exc:
        raise RuntimeError("Database is unavailable") from exc
