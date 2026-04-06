from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from app.notification.application.commands.notification_command import (
    ProcessIncomingNotificationEventCommand,
)
from app.notification.domain.entities.content import NotificationContent
from app.notification.domain.entities.models import Notification
from app.notification.domain.entities.recipient import Recipient
from app.notification.domain.enums import (
    NotificationAttentionStatus,
    NotificationChannel,
    NotificationType,
)
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.sending_service import SendingService
from app.notification.domain.user_profile_service import UserProfileService

logger = logging.getLogger("app")

IMPORTANT_EVENT_KEYWORDS = ("failed", "deleted", "banned", "fraud", "chargeback", "alert")
IMPORTANT_EVENT_TYPES = {
    "user.lifecycle.deleted",
    "user.lifecycle.banned",
    "payment.failed",
    "wallet.payment_failed",
}
STORE_ONLY_EVENT_TYPES = {
    "user.lifecycle.deleted",
}


@dataclass(slots=True)
class RoutingDecision:
    notification_type: NotificationType
    channel: NotificationChannel
    subject: str
    body: str
    should_send: bool
    is_important: bool
    payload_data: dict[str, Any] = field(default_factory=dict)


class ProcessIncomingNotificationEventUseCase:
    """Routes Kafka incoming events into local notifications + optional delivery."""

    def __init__(
        self,
        repository: NotificationRepository,
        sending_service: SendingService,
        user_profile_service: UserProfileService | None = None,
    ) -> None:
        self._repository = repository
        self._sending_service = sending_service
        self._user_profile_service = user_profile_service

    async def execute(self, command: ProcessIncomingNotificationEventCommand) -> None:
        existing = await self._repository.get_by_event_id(command.event_id)
        if existing is not None:
            logger.info(
                "incoming_notification_event.duplicate_skipped event_type=%s event_id=%s notification_id=%s",
                command.event_type,
                command.event_id,
                existing.notification_id,
            )
            return

        payload = command.payload or {}
        recipient = await self._resolve_recipient(payload)
        decision = self._route_event(command.event_type, payload)

        notification = Notification(
            notification_type=decision.notification_type,
            recipient=recipient,
            content=NotificationContent(
                subject=decision.subject,
                body=decision.body,
                data=decision.payload_data,
            ),
            channel=decision.channel,
            event_id=command.event_id,
            source=command.source,
            source_event_type=command.event_type,
            correlation_id=command.correlation_id,
            is_important=decision.is_important,
            attention_status=(
                NotificationAttentionStatus.OPEN
                if decision.is_important
                else NotificationAttentionStatus.NONE
            ),
            metadata={
                "incoming_payload": payload,
                "occurred_at": command.occurred_at.isoformat(),
            },
        )

        saved = await self._repository.save(notification)
        logger.info(
            "incoming_notification_event.stored notification_id=%s event_type=%s event_id=%s important=%s",
            saved.notification_id,
            command.event_type,
            command.event_id,
            decision.is_important,
        )

        if not decision.should_send:
            return
        if decision.channel == NotificationChannel.EMAIL and not saved.recipient.email:
            saved.mark_as_failed("Recipient email not available for delivery.")
            saved.mark_attention_open()
            await self._repository.update(saved)
            return
        if decision.channel == NotificationChannel.SMS and not saved.recipient.phone_number:
            saved.mark_as_failed("Recipient phone_number not available for delivery.")
            saved.mark_attention_open()
            await self._repository.update(saved)
            return

        try:
            await self._sending_service.send_notification(saved)
            saved.mark_as_sent()
        except Exception as exc:
            saved.mark_as_failed(error_details=str(exc))
            saved.mark_attention_open()
        await self._repository.update(saved)

    async def _resolve_recipient(self, payload: dict[str, Any]) -> Recipient:
        user_id = str(payload.get("user_id") or payload.get("recipient_id") or "unknown")
        email = payload.get("email")
        phone_number = payload.get("phone_number") or payload.get("phone")

        if (not email and not phone_number) and self._user_profile_service is not None:
            profile = await self._user_profile_service.resolve_contact(user_id)
            if profile is not None:
                email = email or profile.email
                phone_number = phone_number or profile.phone_number

        return Recipient(
            user_id=user_id,
            email=email,
            phone_number=phone_number,
        )

    def _route_event(self, event_type: str, payload: dict[str, Any]) -> RoutingDecision:
        event_type_normalized = event_type.strip().lower()
        is_important = self._is_important_event(event_type_normalized, payload)
        requested_channel = str(payload.get("channel", "EMAIL")).upper()
        channel = self._safe_channel(requested_channel)
        notification_type = self._resolve_notification_type(event_type_normalized, payload)
        should_send = event_type_normalized not in STORE_ONLY_EVENT_TYPES
        if payload.get("notify") is False:
            should_send = False
        if payload.get("notify") is True:
            should_send = True

        subject = str(payload.get("subject") or self._default_subject(event_type_normalized))
        body = str(payload.get("body") or self._default_body(event_type_normalized, payload))

        if not should_send:
            channel = NotificationChannel.IN_APP

        return RoutingDecision(
            notification_type=notification_type,
            channel=channel,
            subject=subject,
            body=body,
            should_send=should_send,
            is_important=is_important,
            payload_data=dict(payload),
        )

    def _resolve_notification_type(
        self, event_type: str, payload: dict[str, Any]
    ) -> NotificationType:
        raw = payload.get("notification_type")
        if isinstance(raw, str):
            try:
                return NotificationType(raw)
            except ValueError:
                pass

        if "two_factor" in event_type or "auth" in event_type:
            return NotificationType.ACCOUNT_AUTH
        if "ticket" in event_type:
            return NotificationType.TICKET_BUY
        if "product" in event_type:
            return NotificationType.PRODUCT_BUY
        if "created" in event_type or "signed_up" in event_type:
            return NotificationType.ACCOUNT_CREATED
        if "deleted" in event_type:
            return NotificationType.ACCOUNT_DELETED
        if "failed" in event_type:
            return NotificationType.PAYMENT_FAILED
        return NotificationType.CUSTOM_MESSAGE

    def _is_important_event(self, event_type: str, payload: dict[str, Any]) -> bool:
        if payload.get("is_important") is True:
            return True
        if event_type in IMPORTANT_EVENT_TYPES:
            return True
        return any(keyword in event_type for keyword in IMPORTANT_EVENT_KEYWORDS)

    @staticmethod
    def _safe_channel(raw_channel: str) -> NotificationChannel:
        try:
            return NotificationChannel(raw_channel)
        except ValueError:
            return NotificationChannel.EMAIL

    @staticmethod
    def _default_subject(event_type: str) -> str:
        return f"Notification event: {event_type}"

    @staticmethod
    def _default_body(event_type: str, payload: dict[str, Any]) -> str:
        user_id = payload.get("user_id") or payload.get("recipient_id") or "unknown"
        return f"Event '{event_type}' was received for user '{user_id}'."
