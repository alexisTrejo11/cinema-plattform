"""
PostgreSQL checks before the app accepts traffic.

If validation fails, startup aborts so bad deployments fail fast.
"""

from __future__ import annotations

import logging
import sys
from typing import FrozenSet

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config.app_config import settings

logger = logging.getLogger("app")


def _required_table_names() -> FrozenSet[str]:
    # Import models so SQLAlchemy metadata is fully populated.
    import app.users.infrastructure.persistence.models  # noqa: F401

    from app.config.postgres_config import Base

    return frozenset(Base.metadata.tables.keys())


async def validate_postgres(engine: AsyncEngine) -> None:
    """
    Ping PostgreSQL and assert expected ORM tables exist.
    """
    required = _required_table_names()
    if not required:
        logger.warning("No ORM tables registered on Base; skipping schema checks.")

    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

        if not required:
            logger.info("PostgreSQL connectivity check passed.")
            return

        def _existing_tables(sync_conn) -> set[str]:
            return set(inspect(sync_conn).get_table_names())

        existing: set[str] = await conn.run_sync(_existing_tables)

    missing = required - existing
    if missing:
        raise RuntimeError(
            f"Database schema incomplete. Missing table(s): {sorted(missing)}. "
            "Run migrations before starting the service."
        )

    logger.info(
        "PostgreSQL validation passed: connectivity and %d table(s) verified.",
        len(required),
    )


async def run_postgres_startup_check(engine: AsyncEngine) -> None:
    """
    Validate DB during startup and terminate process on failure.
    """
    if not settings.POSTGRES_VALIDATE_ON_STARTUP:
        logger.info(
            "PostgreSQL startup validation skipped (POSTGRES_VALIDATE_ON_STARTUP=false)."
        )
        return

    try:
        await validate_postgres(engine)
    except Exception as exc:
        logger.critical(
            "PostgreSQL startup validation failed. Refusing to start: %s",
            exc,
            exc_info=True,
        )
        sys.exit(1)
