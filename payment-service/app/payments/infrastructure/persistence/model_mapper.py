from decimal import Decimal
from typing import Any, Optional

from app.payments.domain.entities import Payment
from app.payments.domain.value_objects import (
    Currency,
    Money,
    PaymentId,
    PaymentMetadata,
    PaymentMethod,
    PaymentReference,
    PaymentStatus,
    PaymentType,
    UserId,
)
from .models import PaymentModel


def _external_reference_from_storage(raw: Any) -> Optional[PaymentReference]:
    if raw is None:
        return None
    if isinstance(raw, PaymentReference):
        return raw
    if isinstance(raw, dict):
        return PaymentReference.model_validate(raw)
    if isinstance(raw, str):
        if ":" in raw:
            provider, ref = raw.split(":", 1)
            return PaymentReference(provider=provider, reference_id=ref)
        return PaymentReference(provider="stripe", reference_id=raw)
    return None


def _metadata_from_storage(raw: Any) -> Optional[PaymentMetadata]:
    if raw is None:
        return None
    if isinstance(raw, PaymentMetadata):
        return raw
    return PaymentMetadata.model_validate(raw)


class ModelMapper:
    @staticmethod
    def model_to_entity(model: "PaymentModel") -> Payment:
        refund_reasons = model.refund_reasons
        if not refund_reasons:
            refund_reasons = []

        return Payment(
            id=PaymentId.from_string(model.id),
            user_id=UserId.from_string(model.user_id),
            amount=Money(Decimal(model.amount), Currency(model.currency)),
            payment_method=PaymentMethod(model.payment_method),
            payment_type=PaymentType(model.payment_type),
            status=PaymentStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
            completed_at=model.completed_at,
            external_reference=_external_reference_from_storage(model.external_reference),
            metadata=_metadata_from_storage(model.payment_metadata),
            failure_reason=model.failure_reason,
            stripe_payment_intent_id=model.stripe_payment_intent_id,
            refunded_amount=(
                Money(Decimal(str(model.refunded_amount)), Currency(model.currency))
                if model.refunded_amount is not None
                else None
            ),
            refund_reasons=refund_reasons,
            refunded_at=model.refunded_at,
        )

    @staticmethod
    def entity_to_model(entity: Payment) -> PaymentModel:
        return PaymentModel(
            id=str(entity.id.value),
            user_id=str(entity.user_id.value),
            amount=Decimal(str(entity.amount.amount)),
            currency=entity.amount.currency.value,
            refunded_amount=(
                Decimal(str(entity.refunded_amount.amount))
                if entity.refunded_amount is not None
                else None
            ),
            payment_method=entity.payment_method.value,
            payment_type=entity.payment_type.value,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            expires_at=entity.expires_at,
            completed_at=entity.completed_at,
            external_reference=(
                str(entity.external_reference) if entity.external_reference else None
            ),
            stripe_payment_intent_id=entity.stripe_payment_intent_id,
            payment_metadata=(
                entity.metadata.model_dump(mode="json") if entity.metadata else None
            ),
            failure_reason=entity.failure_reason,
            refund_reasons=list(entity.refund_reasons),
            refunded_at=entity.refunded_at,
        )
