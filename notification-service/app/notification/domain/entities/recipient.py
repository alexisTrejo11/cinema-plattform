from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class Recipient(BaseModel):
    """Recipient value object."""

    model_config = ConfigDict(extra="forbid")

    user_id: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    device_token: Optional[str] = None

    @model_validator(mode="after")
    def validate_contact_method(self) -> "Recipient":
        if not any([self.email, self.phone_number, self.device_token]):
            raise ValueError(
                "Recipient requires at least one contact method (email, phone_number, device_token)."
            )
        return self
