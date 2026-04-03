from __future__ import annotations
from typing import List
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from app.config.postgres_config import Base
from app.theater.domain.enums import SeatType, TheaterType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.showtime.infrastructure.persistence.sqlalchemy import ShowtimeSeatModel
    from app.cinema.infrastructure.persistence.sqlalchemy import CinemaModel
    from app.showtime.infrastructure.persistence.sqlalchemy import ShowtimeModel


class TheaterSeatModel(Base):
    """
    SQLAlchemy ORM model for the 'theater_seats' table.
    """

    __tablename__ = "theater_seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    theater_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("theaters.id", ondelete="CASCADE"), nullable=False
    )
    seat_row: Mapped[str] = mapped_column(String(5), nullable=False)
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_type: Mapped[SeatType] = mapped_column(
        SqlEnum(SeatType, name="seat_type_enum", create_type=False),
        nullable=False,
        default=SeatType.STANDARD,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    theater = relationship("TheaterModel", back_populates="theater_seats")
    showtime_bookings = relationship("ShowtimeSeatModel", back_populates="theater_seat")

    __table_args__ = (
        UniqueConstraint(
            "theater_id", "seat_row", "seat_number", name="uq_theater_seat_position"
        ),
    )

    def __repr__(self):
        return f"<TheaterSeat(id={self.id}, theater_id={self.theater_id}, row='{self.seat_row}', number={self.seat_number}, type='{self.seat_type}')>"


class TheaterModel(Base):
    __tablename__ = "theaters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    theater_type: Mapped[TheaterType] = mapped_column(
        SqlEnum(TheaterType, name="theater_type_enum", create_type=False),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    maintenance_mode: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    cinema: Mapped["CinemaModel"] = relationship(back_populates="theaters")
    showtimes: Mapped[List["ShowtimeModel"]] = relationship(back_populates="theater")

    theater_seats: Mapped["ShowtimeSeatModel"] = relationship(
        "TheaterSeatModel",
        back_populates="theater",
        lazy="select",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Theater(id={self.id}, name='{self.name}', type='{self.theater_type.value}')>"
