from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..enums import NotificationChannel, NotificationStatus, NotificationType
from .content import NotificationContent
from .recipient import Recipient


class Notification(BaseModel):
    """Domain aggregate for a notification lifecycle."""

    model_config = ConfigDict(validate_assignment=True)

    notification_id: str = Field(default_factory=lambda: str(uuid4()))
    notification_type: NotificationType
    recipient: Recipient
    content: NotificationContent
    channel: NotificationChannel
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: Optional[str] = None
    status: NotificationStatus = NotificationStatus.PENDING
    sent_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_details: Optional[str] = None
    provider_response: Optional[str] = None

    @model_validator(mode="after")
    def validate_identifier(self) -> "Notification":
        if not self.notification_id:
            raise ValueError("notification_id is required.")
        return self

    def mark_as_sent(self, sent_at: Optional[datetime] = None) -> None:
        self.status = NotificationStatus.SENT
        self.sent_at = sent_at or datetime.now(timezone.utc)
        self.failed_at = None
        self.error_details = None

    def mark_as_failed(
        self,
        error_details: str,
        failed_at: Optional[datetime] = None,
        provider_response: Optional[str] = None,
    ) -> None:
        self.status = NotificationStatus.FAILED
        self.failed_at = failed_at or datetime.now(timezone.utc)
        self.error_details = error_details
        self.provider_response = provider_response
        self.sent_at = None

    def to_document(self) -> Dict[str, Any]:
        payload = self.model_dump(mode="python")
        payload["notification_type"] = self.notification_type.value
        payload["channel"] = self.channel.value
        payload["status"] = self.status.value
        payload["_id"] = payload.pop("notification_id")
        return payload

    @classmethod
    def from_document(cls, data: Dict[str, Any]) -> "Notification":
        payload = dict(data)
        if "_id" in payload:
            payload["notification_id"] = str(payload.pop("_id"))
        return cls.model_validate(payload)
