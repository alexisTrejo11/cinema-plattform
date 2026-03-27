"""Import ORM models so `Base.metadata` is complete for Alembic and startup checks."""

from app.wallet.infrastructure.persistence.sql.sqlalchemy_models import (  # noqa: F401
    WalletSQLModel,
    WalletTransactionSQLModel,
)
