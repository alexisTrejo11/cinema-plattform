from __future__ import annotations
from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum,
    Numeric,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from app.config.postgres_config import Base
from app.showtime.domain.enums import (
    ShowtimeLanguage,
    ShowtimeType,
    ShowtimeStatus,
)

class ShowtimeSeatModel(Base):
    """
    SQLAlchemy ORM model for the 'showtime_seats' table.
    """

    __tablename__ = "showtime_seats"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(
        Integer, ForeignKey("showtimes.id", ondelete="CASCADE"), nullable=False
    )
    theater_seat_id = Column(Integer, nullable=False)
    taken_at = Column(DateTime(timezone=True), nullable=True)
    transaction_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    showtimes = relationship("ShowtimeModel", back_populates="showtime_seats")

    __table_args__ = (
        UniqueConstraint("showtime_id", "theater_seat_id", name="uq_showtime_seat"),
    )

    def __repr__(self):
        return (
            f"<ShowtimeSeat(id={self.id}, showtime_id={self.showtime_id}, "
            f"theater_seat_id={self.theater_seat_id}, taken_at={self.taken_at})>"
        )


class ShowtimeModel(Base):
    __tablename__ = "showtimes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    theater_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cinema_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    language: Mapped[ShowtimeLanguage] = mapped_column(
        Enum(ShowtimeLanguage, name="showtime_language_enum", create_type=False),
        nullable=False,
    )
    type: Mapped[ShowtimeType] = mapped_column(
        Enum(
            "TRADITIONAL_2D",
            "TRADITIONAL_3D",
            "IMAX_2D",
            "IMAX_3D",
            "4D",
            "4DX",
            "VIP_2D",
            "VIP_3D",
            name="showtime_type_enum",
            create_type=False,
        ),
        nullable=False,
    )  # Can't Check Enums Values Cause Naming
    status: Mapped[ShowtimeStatus] = mapped_column(
        Enum(
            "DRAFT",
            "UPCOMING",
            "IN_PROGRESS",
            "COMPLETED",
            "CANCELLED",
            name="showtime_status_enum",
            create_type=False,
        ),
        nullable=False,
        default="DRAFT",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    showtime_seats: Mapped["ShowtimeSeatModel"] = relationship(
        "ShowtimeSeatModel", back_populates="showtimes"
    )

    def __repr__(self) -> str:
        return f"<Showtime(id={self.id}, movie_id={self.movie_id}, theater_id={self.theater_id}, start_time='{self.start_time}')>"
