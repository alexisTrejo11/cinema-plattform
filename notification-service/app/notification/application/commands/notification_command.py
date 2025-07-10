from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from app.notification.domain.enums import NotificationChannel, NotificationType
from app.notification.domain.entities.content import NotificationContent
from app.notification.domain.entities.recipient import Recipient


class CreateNotificationCommand(BaseModel):
    """
    Command to create and send a new notification.
    This command represents the intent to initiate a notification delivery.
    """

    notification_type: NotificationType = Field(
        ..., description="The type of notification."
    )
    recipient: Recipient = Field(
        ..., description="Details of the notification recipient."
    )
    content: NotificationContent = Field(
        ..., description="The content of the notification."
    )
    channel: NotificationChannel = Field(
        ..., description="The preferred channel for notification delivery."
    )

    # Optional fields for traceability and context
    event_id: Optional[UUID4] = Field(
        None, description="Optional ID of the event that triggered this notification."
    )
    correlation_id: Optional[UUID4] = Field(
        None, description="ID for correlating operations across services."
    )
    causation_id: Optional[UUID4] = Field(
        None,
        description="ID of the preceding event or command that caused this command.",
    )
    issued_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when this command was issued.",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "notification_type": "transactional",
                "recipient": {
                    "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                    "email": "testuser@example.com",
                },
                "content": {
                    "subject": "Welcome to Our Service!",
                    "body": "Thank you for registering. We're excited to have you!",
                    "html_body": "<h3>Welcome!</h3><p>Thank you for registering.</p>",
                },
                "channel": "email",
                "event_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            }
        }
