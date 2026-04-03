from __future__ import annotations
from datetime import datetime, date, timezone
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import (
    ARRAY,
    String,
    Integer,
    Boolean,
    DateTime,
    Date,
    Text,
    Float,
    Enum as SQLEnum,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.config.postgres_config import Base
from app.cinema.domain.enums import LocationRegion, CinemaType, CinemaStatus

if TYPE_CHECKING:
    from app.theater.infrastructure.persistence.sqlalchemy import TheaterModel


class CinemaModel(Base):
    __tablename__ = "cinemas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Cinema Info
    image: Mapped[str] = mapped_column(Text, nullable=False, default="")
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    tax_number: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    screens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Dates/Timestamps
    last_renovation: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    # Enums
    type: Mapped[CinemaType] = mapped_column(
        SQLEnum(CinemaType, name="cinema_type_enum", create_type=False), nullable=False
    )
    status: Mapped[CinemaStatus] = mapped_column(
        SQLEnum(CinemaStatus, name="cinema_status_enum", create_type=False),
        nullable=False,
    )
    region: Mapped[LocationRegion] = mapped_column(
        SQLEnum(LocationRegion, name="location_region_enum", create_type=False),
        nullable=False,
    )

    # Amenities
    has_parking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_food_court: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_coffee_station: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    has_disabled_access: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    # Contact Info
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email_contact: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Location
    latitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)

    # Social Media URLs
    facebook_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instagram_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    x_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tik_tok_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Features
    features: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )  # PRODUCTION
    # features: Mapped[StringList] = mapped_column(StringList, nullable=False, default=list) # TEST

    theaters: Mapped[List["TheaterModel"]] = relationship(
        back_populates="cinema", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<CinemaModel(id={self.id}, name='{self.name}', status='{self.status.value}', "
            f"latitude={self.latitude}, longitude={self.longitude})>"
        )
