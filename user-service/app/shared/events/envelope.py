"""
Canonical envelope for all messages published to Kafka from user-service.

Consumers (notification service, monitoring, etc.) should filter by ``event_type``.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Stable identifiers for downstream routing."""

    # Notification service — send email / SMS / push
    NOTIFICATION_REQUESTED = "notification.requested"

    # Auth — 2FA / OTP flows (no secrets; notification service may send codes)
    TWO_FACTOR_CHALLENGE_ISSUED = "user.auth.two_factor_challenge_issued"

    # User lifecycle — monitoring & audit
    USER_SIGNED_UP = "user.lifecycle.signed_up"
    USER_CREATED = "user.lifecycle.created"
    USER_UPDATED = "user.lifecycle.updated"
    USER_DELETED = "user.lifecycle.deleted"
    USER_ACTIVATED = "user.lifecycle.activated"
    USER_BANNED = "user.lifecycle.banned"
    TWO_FACTOR_ENABLED = "user.auth.two_factor_enabled"
    TWO_FACTOR_DISABLED = "user.auth.two_factor_disabled"


class DomainEventEnvelope(BaseModel):
    """
    Single JSON document per Kafka message value.
    """

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    source: str = "user-service"
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp",
    )
    correlation_id: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}
