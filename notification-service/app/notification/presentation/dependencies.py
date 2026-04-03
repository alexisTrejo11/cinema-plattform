from fastapi import Depends

from app.config.mongo_config import get_mongo_database
from app.notification.application.usecases.notification_usecases import (
    CreateNotificationUseCase,
    GetNotificationByIdUseCase,
    ListNotificationsUseCase,
)
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.sending_service import SendingService
from app.notification.infrastructure.email.mail_service import EmailService
from app.notification.infrastructure.message.sms_message_services import SmsMessageService
from app.notification.infrastructure.repository.mongo_notification_repository import (
    MongoNotificationRepository,
)
from app.notification.infrastructure.services import SendingServiceImplementation


async def get_notification_repository(
    db=Depends(get_mongo_database),
) -> NotificationRepository:
    return MongoNotificationRepository(db)


def get_sending_service() -> SendingService:
    return SendingServiceImplementation(
        email_service=EmailService(),
        sms_service=SmsMessageService(),
    )


def get_create_notification_usecase(
    repo: NotificationRepository = Depends(get_notification_repository),
    sending_service: SendingService = Depends(get_sending_service),
) -> CreateNotificationUseCase:
    return CreateNotificationUseCase(repository=repo, sending_service=sending_service)


def get_notification_by_id_usecase(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> GetNotificationByIdUseCase:
    return GetNotificationByIdUseCase(repository=repo)


def get_list_notifications_usecase(
    repo: NotificationRepository = Depends(get_notification_repository),
) -> ListNotificationsUseCase:
    return ListNotificationsUseCase(repository=repo)
