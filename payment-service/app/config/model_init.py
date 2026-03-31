"""Import ORM models so Base.metadata is complete for Alembic and startup checks."""

from app.payments.infrastructure.persistence.models import PaymentModel  # noqa: F401
