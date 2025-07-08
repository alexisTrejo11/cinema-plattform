from dataclasses import dataclass, field
from datetime import datetime
from app.domain.value_objects.id import ID
from app.domain.value_objects.card import Card

@dataclass
class PaymentMethod:
    id: ID
    user_id: str
    card: Card
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime = None

