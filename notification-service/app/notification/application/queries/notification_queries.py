from pydantic import BaseModel, ConfigDict, Field

from app.notification.domain.enums import (
    NotificationAttentionStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)


class GetNotificationByIdQuery(BaseModel):
    """Query to retrieve a single notification by its ID."""

    model_config = ConfigDict(extra="forbid")
    notification_id: str = Field(..., min_length=1)


class ListNotificationsQuery(BaseModel):
    """Query DTO with optional filters."""

    model_config = ConfigDict(extra="forbid")

    notification_type: NotificationType | None = None
    channel: NotificationChannel | None = None
    user_id: str | None = None
    status: NotificationStatus | None = None
    is_important: bool | None = None
    attention_status: NotificationAttentionStatus | None = None
    source_event_type: str | None = None
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)
