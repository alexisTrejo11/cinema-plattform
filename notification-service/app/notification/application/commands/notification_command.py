from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.notification.domain.entities.content import NotificationContent
from app.notification.domain.entities.recipient import Recipient
from app.notification.domain.enums import NotificationChannel, NotificationType


class CreateNotificationCommand(BaseModel):
    """DTO for notification creation requests."""

    model_config = ConfigDict(extra="forbid")

    notification_type: NotificationType
    recipient: Recipient
    content: NotificationContent
    channel: NotificationChannel
    event_id: Optional[str] = None
    correlation_id: Optional[UUID] = None
    causation_id: Optional[UUID] = None
    source: Optional[str] = None
    source_event_type: Optional[str] = None
    is_important: bool = False
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProcessIncomingNotificationEventCommand(BaseModel):
    """DTO used by Kafka consumers for external incoming events."""

    model_config = ConfigDict(extra="allow")

    event_type: str
    event_id: str
    payload: dict
    source: str = "unknown"
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
