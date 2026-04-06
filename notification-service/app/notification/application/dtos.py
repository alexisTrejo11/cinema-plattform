from datetime import datetime
from typing import Any, Optional, Dict, List
from pydantic import BaseModel, ConfigDict, Field
from app.notification.domain.enums import (
    NotificationAttentionStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)


class RecipientResponse(BaseModel):
    """Recipient information for the notification"""

    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(..., description="Unique identifier of the recipient")
    email: Optional[str] = Field(None, description="Email address of the recipient")
    phone_number: Optional[str] = Field(
        None, description="Phone number of the recipient"
    )
    device_token: Optional[str] = Field(
        None, description="Device token for push notifications"
    )


class NotificationContentResponse(BaseModel):
    """Content of the notification"""

    model_config = ConfigDict(from_attributes=True)

    subject: str = Field(..., description="Subject line or title of the notification")
    body: str = Field(..., description="Main content of the notification")
    template_name: Optional[str] = Field(None, description="Name of the template used")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional template data")


# Main Response Response
class NotificationResponse(BaseModel):
    """Complete notification response Response"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "notification_id": "notif_12345",
                "notification_type": "TICKET_BUY",
                "recipient": {"user_id": "user_123", "email": "user@example.com"},
                "content": {
                    "subject": "Your Ticket Purchase",
                    "body": "Thank you for your purchase!",
                    "template_name": "ticket_purchase",
                },
                "channel": "EMAIL",
                "status": "SENT",
                "created_at": "2023-01-01T12:00:00Z",
                "sent_at": "2023-01-01T12:00:05Z",
            }
        },
    )

    notification_id: str = Field(
        ..., description="Unique identifier of the notification"
    )
    notification_type: NotificationType = Field(..., description="Type of notification")
    recipient: RecipientResponse = Field(..., description="Recipient information")
    content: NotificationContentResponse = Field(
        ..., description="Notification content"
    )
    channel: NotificationChannel = Field(..., description="Delivery channel")
    status: NotificationStatus = Field(
        default=NotificationStatus.PENDING, description="Current status"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    event_id: Optional[str] = Field(None, description="Associated event ID")
    sent_at: Optional[datetime] = Field(None, description="When notification was sent")
    failed_at: Optional[datetime] = Field(None, description="When notification failed")
    error_details: Optional[str] = Field(None, description="Error details if failed")
    provider_response: Optional[str] = Field(None, description="Raw provider response")
    source: Optional[str] = Field(None, description="Source service name")
    source_event_type: Optional[str] = Field(
        None, description="Original integration event type"
    )
    correlation_id: Optional[str] = Field(
        None, description="Correlation ID for distributed tracing"
    )
    causation_id: Optional[str] = Field(
        None, description="Causation ID for event chaining"
    )
    is_important: bool = Field(
        default=False, description="Marks records that need easy monitoring."
    )
    attention_status: NotificationAttentionStatus = Field(
        default=NotificationAttentionStatus.NONE,
        description="Operational follow-up state for important alerts.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional event context."
    )


class NotificationListResponse(BaseModel):
    """
    DTO for a list of notifications.
    """

    notifications: List[NotificationResponse]
    total_count: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notifications": [
                    {
                        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                        "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                        "type": "transactional",
                        "channel": "email",
                        "message": "Your order #123 has been shipped!",
                        "status": "sent",
                        "created_at": "2025-07-08T10:00:00Z",
                        "sent_at": "2025-07-08T10:05:00Z",
                        "read_at": None,
                    },
                    {
                        "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef0",
                        "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                        "type": "promotional",
                        "channel": "push",
                        "message": "Check out our new summer deals!",
                        "status": "pending",
                        "created_at": "2025-07-09T09:00:00Z",
                        "sent_at": None,
                        "read_at": None,
                    },
                ],
                "total_count": 2,
            }
        }
    )
