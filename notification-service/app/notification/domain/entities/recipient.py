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
        if not self.user_id.strip():
            raise ValueError("Recipient user_id is required.")
        return self
