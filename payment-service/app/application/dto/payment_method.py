from dataclasses import dataclass
from datetime import datetime
from app.domain.entities.payment_method import PaymentMethod

@dataclass
class PaymentMethodDTO:
    id: str
    user_id: str
    card_holder: str
    card_number: str
    expiration_month: str
    expiration_year: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime = None

    @staticmethod
    def from_entity(payment_method: PaymentMethod) -> "PaymentMethodDTO":
        return PaymentMethodDTO(
            id=str(payment_method.id),
            user_id=payment_method.user_id,
            card_holder=payment_method.card.card_holder,
            card_number=payment_method.card.card_number,
            expiration_month=payment_method.card.expiration_month,
            expiration_year=payment_method.card.expiration_year,
            created_at=payment_method.created_at,
            updated_at=payment_method.updated_at,
            deleted_at=payment_method.deleted_at
        )

