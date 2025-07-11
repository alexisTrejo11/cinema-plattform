from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List


class GetNotificationByIdQuery(BaseModel):
    """Query to retrieve a single notification by its ID."""

    notification_id: UUID = Field(
        ..., description="ID of the notification to retrieve."
    )


class ListNotificationsByTypeQuery(BaseModel):
    """Query to list notifications by their type."""

    notification_type: str = Field(
        ...,
        description="Type of notifications to list (e.g., 'promotional', 'transactional').",
    )
    limit: int = Field(
        10, gt=0, le=100, description="Maximum number of notifications to return."
    )
    offset: int = Field(0, ge=0, description="Number of notifications to skip.")


class ListNotificationsByChannelQuery(BaseModel):
    """Query to list notifications by their channel."""

    channel: str = Field(
        ..., description="Channel of notifications to list (e.g., 'email', 'sms')."
    )
    limit: int = Field(
        10, gt=0, le=100, description="Maximum number of notifications to return."
    )
    offset: int = Field(0, ge=0, description="Number of notifications to skip.")


class ListNotificationsByUserIdQuery(BaseModel):
    """Query to list notifications for a specific user ID."""

    user_id: str = Field(
        ..., description="ID of the user whose notifications to retrieve."
    )
    limit: int = Field(
        10, gt=0, le=100, description="Maximum number of notifications to return."
    )
    offset: int = Field(0, ge=0, description="Number of notifications to skip.")


class ListNotificationsByStatusQuery(BaseModel):
    """Query to list notifications by their status."""

    status: str = Field(
        ..., description="Status of notifications to list (e.g., 'pending', 'sent')."
    )
    limit: int = Field(
        10, gt=0, le=100, description="Maximum number of notifications to return."
    )
    offset: int = Field(0, ge=0, description="Number of notifications to skip.")
