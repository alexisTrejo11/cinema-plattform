from fastapi import Depends
from app.domain.repository import NotificationRepository
from config.mongo_config import get_mongo_database
from app.infrastructure.persistence.mongo_notification_repository import (
    MongoNotificationRepository,
)
from app.application.queries.notification_query_handler import (
    GetNotificationByIdQueryHandler,
    ListNotificationsByStatusQueryHandler,
    ListNotificationsByUserIdQueryHandler,
    ListNotificationsByTypeQueryHandler,
    ListNotificationsByChannelQueryHandler,
)


async def get_notification_repository(
    db=Depends(get_mongo_database),
) -> NotificationRepository:
    """Provides a NotificationRepository instance."""
    return MongoNotificationRepository(db)


def get_get_notification_by_id_handler(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> GetNotificationByIdQueryHandler:
    return GetNotificationByIdQueryHandler(repository=repo)


def get_list_notifications_by_type_handler(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> ListNotificationsByTypeQueryHandler:
    return ListNotificationsByTypeQueryHandler(repository=repo)


def get_list_notifications_by_channel_handler(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> ListNotificationsByChannelQueryHandler:
    return ListNotificationsByChannelQueryHandler(repository=repo)


def get_list_notifications_by_user_id_handler(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> ListNotificationsByUserIdQueryHandler:
    return ListNotificationsByUserIdQueryHandler(repository=repo)


def get_list_notifications_by_status_handler(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> ListNotificationsByStatusQueryHandler:
    return ListNotificationsByStatusQueryHandler(repository=repo)
