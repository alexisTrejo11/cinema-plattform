from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.notification.application.commands.notification_command import (
    CreateNotificationCommand,
)
from app.notification.application.dtos import (
    NotificationListResponse,
    NotificationResponse,
)
from app.notification.application.queries.notification_queries import (
    GetNotificationByIdQuery,
    ListNotificationsQuery,
)
from app.notification.application.usecases.notification_usecases import (
    CreateNotificationUseCase,
    GetNotificationByIdUseCase,
    ListNotificationsUseCase,
)
from app.notification.domain.enums import (
    NotificationAttentionStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)

from .dependencies import (
    get_create_notification_usecase,
    get_list_notifications_usecase,
    get_notification_by_id_usecase,
)


router = APIRouter(prefix="/api/v2/notifications")


@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    command: CreateNotificationCommand,
    usecase: CreateNotificationUseCase = Depends(get_create_notification_usecase),
):
    return await usecase.execute(command)


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification_by_id(
    notification_id: str,
    usecase: GetNotificationByIdUseCase = Depends(get_notification_by_id_usecase),
):
    query = GetNotificationByIdQuery(notification_id=notification_id)
    notification = await usecase.execute(query)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )
    return notification


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    notification_type: NotificationType | None = None,
    channel: NotificationChannel | None = None,
    user_id: str | None = None,
    status_filter: NotificationStatus | None = Query(default=None, alias="status"),
    is_important: bool | None = Query(default=None),
    attention_status: NotificationAttentionStatus | None = Query(default=None),
    source_event_type: str | None = Query(default=None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    usecase: ListNotificationsUseCase = Depends(get_list_notifications_usecase),
):
    query = ListNotificationsQuery(
        notification_type=notification_type,
        channel=channel,
        user_id=user_id,
        status=status_filter,
        is_important=is_important,
        attention_status=attention_status,
        source_event_type=source_event_type,
        limit=limit,
        offset=offset,
    )
    return await usecase.execute(query)
