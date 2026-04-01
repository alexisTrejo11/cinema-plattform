from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Numeric, DateTime, Text, JSON, Boolean

from app.config.postgres_config import Base


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    refunded_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), default=0.0
    )

    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    refunded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    external_reference: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    payment_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata", JSON, nullable=True
    )
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refund_reasons: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)


class PaymentMethodModel(Base):
    __tablename__ = "payment_methods"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    stripe_code: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    min_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
