"""Import ORM models so `Base.metadata` is complete for Alembic and startup checks."""

from app.ticket.infrastructure.persistence.models import (  # noqa: F401
    ShowtimeSeatModel,
    TicketModel,
)
