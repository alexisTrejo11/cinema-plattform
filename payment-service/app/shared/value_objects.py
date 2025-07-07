from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4
from typing import Annotated, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, AfterValidator, model_validator, condecimal, StringConstraints
from pydantic_core import PydanticCustomError

class TransactionSource(StrEnum):
    SYSTEM = "system"
    PAYMENT = "payment"
    REFUND = "refund"
    PROMOTION = "promotion"
    MANUAL = "manual"

PositiveDecimal = Annotated[
    condecimal(gt=0, decimal_places=2),
    AfterValidator(lambda v: v.quantize(Decimal('0.00')))
]

TransactionReference = Annotated[
    str,
    StringConstraints(min_length=1, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
]
