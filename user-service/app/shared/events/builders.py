"""
Factory helpers that map domain objects to ``DomainEventEnvelope`` instances.
"""

from __future__ import annotations

from typing import Any, Optional

from app.shared.events.envelope import DomainEventEnvelope, EventType
from app.shared.notification.domain.entities import Notification
from app.users.domain import User


def notification_requested(notification: Notification) -> DomainEventEnvelope:
    """Email/SMS/push request for notification-service to deliver."""
    user = notification.user
    payload: dict[str, Any] = {
        "notification_type": notification.notification_type.value,
        "user_id": user.id,
        "email": str(user.email),
        "token": notification.token,
    }
    if user.phone_number is not None:
        payload["phone_number"] = str(user.phone_number)
    return DomainEventEnvelope(
        event_type=EventType.NOTIFICATION_REQUESTED,
        payload=payload,
    )


def two_factor_challenge_issued(
    user: User,
    *,
    reason: str,
    correlation_id: Optional[str] = None,
) -> DomainEventEnvelope:
    """
    Published when a 2FA challenge is started (e.g. login step-up).
    Does not include TOTP secrets or raw QR payloads.
    """
    return DomainEventEnvelope(
        event_type=EventType.TWO_FACTOR_CHALLENGE_ISSUED,
        correlation_id=correlation_id,
        payload={
            "user_id": user.id,
            "email": str(user.email),
            "reason": reason,
        },
    )


def user_signed_up(user_id: int, email: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_SIGNED_UP,
        payload={"user_id": user_id, "email": email},
    )


def user_created(user_id: int, email: str, role: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_CREATED,
        payload={"user_id": user_id, "email": email, "role": role},
    )


def user_updated(user_id: int, fields_changed: list[str]) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_UPDATED,
        payload={"user_id": user_id, "fields_changed": fields_changed},
    )


def user_deleted(user_id: int) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_DELETED,
        payload={"user_id": user_id},
    )


def user_activated(user_id: int, email: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_ACTIVATED,
        payload={"user_id": user_id, "email": email},
    )


def user_banned(user_id: int, email: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.USER_BANNED,
        payload={"user_id": user_id, "email": email},
    )


def two_factor_enabled(user_id: int, email: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.TWO_FACTOR_ENABLED,
        payload={"user_id": user_id, "email": email},
    )


def two_factor_disabled(user_id: int, email: str) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        event_type=EventType.TWO_FACTOR_DISABLED,
        payload={"user_id": user_id, "email": email},
    )
