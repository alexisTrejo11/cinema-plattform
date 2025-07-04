from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .app_config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.postgres_uri, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_postgres_db():
    async with AsyncSessionLocal() as session:
        yield session
