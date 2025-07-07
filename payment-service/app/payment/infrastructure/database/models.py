from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Numeric, DateTime, Text, JSON

from app.payment.domain.entities.payment import Payment, PaymentId, UserId
from app.payment.domain.value_objects import Currency, Money, PaymentStatus, PaymentType, PaymentMethod


class Base(DeclarativeBase):
    pass


class PaymentModel(Base):
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=True)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    refunded_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), default=0.0)

    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    refunded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    
    external_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSON, nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refund_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    
    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)


class ModelMapper:
    @staticmethod
    def model_to_entity(model: 'PaymentModel') -> Payment:
        """Convert SQLAlchemy PaymentModel to domain Payment entity.
        
        Args:
            model: SQLAlchemy model instance
            
        Returns:
            Domain Payment entity with all fields converted
        """
        
        return Payment(
            id=PaymentId.from_string(model.user_id),
            user_id=UserId.from_string(model.user_id),
            amount=Money(Decimal(model.amount), Currency(model.currency)),
            payment_method=PaymentMethod(model.payment_method),
            payment_type=PaymentType(model.payment_type),
            status=PaymentStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
            completed_at=model.completed_at,
            external_reference=model.external_reference, # Map
            metadata=model.payment_metadata,
            failure_reason=model.failure_reason,
            refunded_amount= Money(model.refunded_amount, Currency(model.currency)) if model.refunded_amount else None,
            refund_reason=model.refund_reason,
            refunded_at=model.refunded_at
        )

    @staticmethod
    def entity_to_model(entity: Payment) -> PaymentModel:
        """Convert domain Payment entity to SQLAlchemy PaymentModel.
        
        Args:
            entity: Domain Payment entity
            
        Returns:
            SQLAlchemy PaymentModel with all fields converted
        """
        return PaymentModel(
            id=entity.id,
            user_id=entity.user_id,
            amount=Decimal(str(entity.amount)),
            currency=entity.amount.currency,
            payment_method=entity.payment_method,
            payment_type=entity.payment_type,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            expires_at=entity.expires_at,
            completed_at=entity.completed_at,
            external_reference=entity.external_reference,
            metadata=entity.metadata,
            failure_reason=entity.failure_reason,
            refunded_amount=Decimal(str(entity.refunded_amount)) if entity.refunded_amount else None,
            refund_reason=entity.refund_reason,
            refunded_at=entity.refunded_at
        )