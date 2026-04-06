import logging

from app.notification.application.commands.notification_command import (
    CreateNotificationCommand,
)
from app.notification.application.dtos import NotificationListResponse, NotificationResponse
from app.notification.application.queries.notification_queries import (
    GetNotificationByIdQuery,
    ListNotificationsQuery,
)
from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import NotificationAttentionStatus
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.sending_service import SendingService

logger = logging.getLogger("app")


class CreateNotificationUseCase:
    def __init__(
        self, repository: NotificationRepository, sending_service: SendingService
    ) -> None:
        self.repository = repository
        self.sending_service = sending_service

    async def execute(self, command: CreateNotificationCommand) -> NotificationResponse:
        notification = Notification(
            notification_type=command.notification_type,
            recipient=command.recipient,
            content=command.content,
            channel=command.channel,
            event_id=command.event_id,
            correlation_id=str(command.correlation_id)
            if command.correlation_id is not None
            else None,
            causation_id=str(command.causation_id)
            if command.causation_id is not None
            else None,
            source=command.source,
            source_event_type=command.source_event_type,
            is_important=command.is_important,
            attention_status=(
                NotificationAttentionStatus.OPEN
                if command.is_important
                else NotificationAttentionStatus.NONE
            ),
        )
        saved = await self.repository.save(notification)
        try:
            await self.sending_service.send_notification(saved)
            saved.mark_as_sent()
        except Exception as exc:
            saved.mark_as_failed(error_details=str(exc))
            if saved.is_important:
                saved.mark_attention_open()
        await self.repository.update(saved)
        logger.info(
            "notification.created id=%s user_id=%s channel=%s type=%s",
            saved.notification_id,
            saved.recipient.user_id,
            saved.channel.value,
            saved.notification_type.value,
        )
        return NotificationResponse.model_validate(saved.model_dump())


class GetNotificationByIdUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def execute(self, query: GetNotificationByIdQuery) -> NotificationResponse | None:
        notification = await self.repository.get_by_id(query.notification_id)
        if notification is None:
            return None
        return NotificationResponse.model_validate(notification.model_dump())


class ListNotificationsUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def execute(self, query: ListNotificationsQuery) -> NotificationListResponse:
        notifications = await self.repository.list_notifications(
            notification_type=query.notification_type,
            channel=query.channel,
            user_id=query.user_id,
            status=query.status,
            is_important=query.is_important,
            attention_status=query.attention_status,
            source_event_type=query.source_event_type,
            limit=query.limit,
            offset=query.offset,
        )
        total_count = await self.repository.count_notifications(
            notification_type=query.notification_type,
            channel=query.channel,
            user_id=query.user_id,
            status=query.status,
            is_important=query.is_important,
            attention_status=query.attention_status,
            source_event_type=query.source_event_type,
        )
        return NotificationListResponse(
            notifications=[
                NotificationResponse.model_validate(item.model_dump())
                for item in notifications
            ],
            total_count=total_count,
        )
