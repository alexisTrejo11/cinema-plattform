from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.ticket.domain.valueobjects.enums import TicketStatus, TicketType
from app.config.postgres_config import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from app.ticket.infrastructure.persistence.models import ShowtimeSeatModel


class TicketModel(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    showtime_id: Mapped[int] = mapped_column(Integer, nullable=False)

    transaction_id: Mapped[int] = mapped_column(Integer, nullable=True)
    payment_id: Mapped[int] = mapped_column(Integer, nullable=True)

    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    customer_ip: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    customer_email: Mapped[str] = mapped_column(String, nullable=True)

    price: Mapped[Decimal] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(String(3), nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)
    ticket_type: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    showtime_seats = relationship(
        "ShowtimeSeatModel", back_populates="ticket", cascade="all, delete-orphan"
    )
