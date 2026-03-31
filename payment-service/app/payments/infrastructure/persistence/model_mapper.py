from app.payments.domain.entities import Payment
from app.payments.domain.value_objects import PaymentId, UserId
from app.payments.domain.value_objects import (
    Currency,
    Money,
    PaymentStatus,
    PaymentType,
    PaymentMethod,
)
from .models import PaymentModel
from decimal import Decimal


class ModelMapper:
    @staticmethod
    def model_to_entity(model: "PaymentModel") -> Payment:
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
            external_reference=model.external_reference,  # Map
            metadata=model.payment_metadata,
            failure_reason=model.failure_reason,
            refunded_amount=(
                Money(model.refunded_amount, Currency(model.currency))
                if model.refunded_amount
                else None
            ),
            refund_reason=model.refund_reason,
            refunded_at=model.refunded_at,
        )

    @staticmethod
    def entity_to_model(entity: Payment) -> PaymentModel:
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
            refunded_amount=(
                Decimal(str(entity.refunded_amount)) if entity.refunded_amount else None
            ),
            refund_reason=entity.refund_reason,
            refunded_at=entity.refunded_at,
        )
