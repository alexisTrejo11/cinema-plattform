"""
Alembic environment configuration.

Supports both:
  • Online mode  – connects to the live database (async engine, asyncpg driver).
  • Offline mode – emits SQL to stdout without a DB connection.

Model discovery
───────────────
Models are imported lazily inside _load_metadata() to avoid failing when
Settings() is constructed without a .env file present (e.g. CI, offline SQL
generation, or running Alembic from an environment where only DATABASE_URL is
set as a plain env-var and not all other settings are present).

For --autogenerate (schema diffing) you do need a fully populated .env.
For applying / reverting explicit migrations (.upgrade / .downgrade) the model
import is attempted but failures are non-fatal — the migration scripts contain
all DDL explicitly via op.create_table() / op.execute().
"""

import asyncio
import os
from logging.config import fileConfig

import sqlalchemy as sa
from sqlalchemy import MetaData, pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# ── Alembic config object ─────────────────────────────────────────────────────
alembic_cfg = context.config

if alembic_cfg.config_file_name is not None:
    fileConfig(alembic_cfg.config_file_name)


# ── Lazy model / metadata loading ─────────────────────────────────────────────


def _load_metadata() -> MetaData:
    """
    Import all SQLAlchemy model modules so their classes register with
    Base.metadata, then return that metadata object.

    Wrapped in try/except because postgres_config creates the async engine at
    module-level (requiring DATABASE_URL in settings). If settings are missing,
    we fall back to an empty MetaData — sufficient for running explicit
    migration scripts; NOT sufficient for --autogenerate.
    """
    try:
        # These imports have side-effects: they register ORM classes with Base.
        from app.config.postgres_config import Base  # noqa: F401
        import app.user.infrastructure.model  # noqa: F401
        import app.wallet.infrastructure.persistence.sql.sqlalchemy_models  # noqa: F401

        return Base.metadata
    except Exception as exc:
        import warnings

        warnings.warn(
            f"Could not load app models ({exc}). "
            "Autogenerate will be empty. "
            "Explicit up/down migrations are unaffected.",
            stacklevel=2,
        )
        return MetaData()


# ── URL resolution ────────────────────────────────────────────────────────────


def _get_async_url() -> str:
    """
    Priority:
      1. ALEMBIC_DATABASE_URL  (explicit override for CI / Docker)
      2. DATABASE_URL          (generic env var)
      3. App settings from .env file
      4. alembic.ini fallback (converted to asyncpg dialect)
    """
    url = os.getenv("ALEMBIC_DATABASE_URL") or os.getenv("DATABASE_URL")

    if not url:
        try:
            from app.config.app_config import settings

            url = settings.DATABASE_URL
        except Exception:
            url = alembic_cfg.get_main_option("sqlalchemy.url", "")

    url = url.replace("postgresql://", "postgresql+asyncpg://")
    url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    return url


def _get_sync_url() -> str:
    """Sync variant used for offline SQL generation (needs only dialect info)."""
    return _get_async_url().replace("postgresql+asyncpg://", "postgresql+psycopg2://")


# ── Offline mode (generate SQL without a live DB connection) ──────────────────


def run_migrations_offline() -> None:
    """
    Emit raw SQL statements to stdout / file.
    Run with:  alembic upgrade head --sql
    """
    context.configure(
        url=_get_sync_url(),
        target_metadata=_load_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online mode (apply changes directly to the database) ─────────────────────


def _do_run_migrations(connection: sa.Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=_load_metadata(),
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Connect with the async engine and apply/revert migrations."""
    engine = create_async_engine(
        _get_async_url(),
        poolclass=pool.NullPool,  # safe for short-lived Alembic runs
    )

    async with engine.connect() as connection:
        await connection.run_sync(_do_run_migrations)

    await engine.dispose()


# ── Entry point ───────────────────────────────────────────────────────────────

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
