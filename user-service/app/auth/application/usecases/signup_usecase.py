import asyncio
import logging

from app.shared.notification.domain.entities import Notification, NotificationType
from app.shared.notification.domain.services import NotificationService
from app.shared.response import Result
from app.shared.token.core import TokenProvider, TokenType
from app.users.application.dtos import UserResponse
from app.users.domain import Status as UserStatus, User, UserRepository

from ..dtos import SignUpRequest
from ..services import AuthValidationService, PasswordService

logger = logging.getLogger(__name__)


class SignUpUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        validation_service: AuthValidationService,
        password_service: PasswordService,
        token_service: TokenProvider,
        notification_service: NotificationService,
    ):
        self.user_repository = user_repository
        self.validation_service = validation_service
        self.password_service = password_service
        self.token_service = token_service
        self.notification_service = notification_service

    async def execute(self, request: SignUpRequest) -> Result[UserResponse]:
        validation_result = await self.validation_service.validate_unique_fields(
            request.email, request.phone_number
        )
        if not validation_result.is_success():
            return validation_result

        new_user = await self._create_user(request)
        asyncio.create_task(self._send_activation_notification(new_user))

        user_response = UserResponse.from_domain(new_user)
        return Result.success(user_response)

    async def _create_user(self, request: SignUpRequest) -> User:
        new_user = User(**request.model_dump())
        new_user.status = UserStatus.PENDING

        hashed_password = self.password_service.hash_password(request.password)
        new_user.password = hashed_password

        created_user = await self.user_repository.save(new_user)
        logger.info("signup user created id=%s", created_user.id)
        return created_user

    async def _send_activation_notification(self, user: User) -> None:
        token = self.token_service.create(TokenType.VERIFICATION, **user.model_dump())
        notification = Notification(user, token.code, NotificationType.EMAIL)
        await self.notification_service.send_notification(notification)
