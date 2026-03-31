from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..value_objects import ID, Card

class PaymentMethod(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ID
    user_id: str
    card: Card
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

