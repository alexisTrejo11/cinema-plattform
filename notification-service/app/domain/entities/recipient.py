from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..enums import *


@dataclass(frozen=True)
class Recipient:
    """
    Value object representing the recipient of a notification.
    """

    user_id: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    device_token: Optional[str] = None

    def __post_init__(self):
        """
        Validates that at least one contact method is provided.
        """
        if not any([self.email, self.phone_number, self.device_token]):
            raise ValueError(
                "Recipient must have at least one contact method (email, phone_number, or device_token)."
            )
