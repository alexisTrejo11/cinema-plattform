from typing import Callable, List

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.app_config import settings
from app.config.postgres_config import get_db
from app.config.cache_config import get_redis_client

from app.auth.application.services import (
    AuthValidationService,
    PasswordService,
    SessionService,
)
from app.auth.application.usecases import AuthUseCasesContainer, build_auth_use_cases
from app.auth.domain.exceptions import InvalidCredentialsException
from app.shared.exceptions import (
    AuthorizationException,
    AuthErrorCode,
    auth_error,
    forbidden_error,
)
from app.shared.events.protocols import EventPublisher
from app.shared.notification.domain.services import NotificationService
from app.shared.notification.infrastructure.services_impl import NotificationServiceImpl
from app.shared.token.core import TokenRepository, TokenProvider
from app.shared.token.infrastructure import TokenProviderImpl, RedisTokenRepository
from app.users.domain import User, UserRepository, UserRole
from app.users.infrastructure.persistence.sqlalch_user_repo import (
    SQLAlchemyUserRepository,
)

security = HTTPBearer(auto_error=False)


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_token_repository(
    redis_client=Depends(get_redis_client),
) -> TokenRepository:
    return RedisTokenRepository(redis_client)


def get_password_service() -> PasswordService:
    return PasswordService()


def get_token_service(
    token_repo: TokenRepository = Depends(get_token_repository),
) -> TokenProvider:
    return TokenProviderImpl(
        token_repository=token_repo,
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def get_auth_validation_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenProvider = Depends(get_token_service),
) -> AuthValidationService:
    return AuthValidationService(user_repo, password_service, token_service)


def get_session_service(
    token_service: TokenProvider = Depends(get_token_service),
) -> SessionService:
    return SessionService(token_service)


def get_event_publisher(request: Request) -> EventPublisher:
    return request.app.state.event_publisher


def get_notification_service(
    publisher: EventPublisher = Depends(get_event_publisher),
) -> NotificationService:
    return NotificationServiceImpl(publisher)


def get_auth_use_cases(
    user_repo: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    validation_service: AuthValidationService = Depends(get_auth_validation_service),
    token_service: TokenProvider = Depends(get_token_service),
    session_service: SessionService = Depends(get_session_service),
    notification_service: NotificationService = Depends(get_notification_service),
    event_publisher: EventPublisher = Depends(get_event_publisher),
) -> AuthUseCasesContainer:
    return build_auth_use_cases(
        user_repo=user_repo,
        password_service=password_service,
        validation_service=validation_service,
        token_service=token_service,
        session_service=session_service,
        notification_service=notification_service,
        event_publisher=event_publisher,
    )


async def get_logged_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    token_service: TokenProvider = Depends(get_token_service),
) -> User:
    if credentials is None:
        raise auth_error(AuthErrorCode.MISSING_BEARER)
    try:
        payload = token_service.verify_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise auth_error(AuthErrorCode.INVALID_TOKEN)

        user = await user_repository.get_by_id(int(user_id))
        if not user:
            raise auth_error(AuthErrorCode.USER_NOT_FOUND)

        return user
    except InvalidCredentialsException:
        raise auth_error(AuthErrorCode.INVALID_CREDENTIALS)
    except AuthorizationException:
        raise
    except Exception:
        raise auth_error(AuthErrorCode.INVALID_CREDENTIALS)


def role_required(required_roles: List[UserRole]) -> Callable[[User], User]:
    def role_checker(logged_user: User = Depends(get_logged_user)) -> User:
        if logged_user.role not in required_roles:
            raise forbidden_error(
                details={
                    "required_roles": [r.value for r in required_roles],
                    "user_role": logged_user.role.value if logged_user.role else None,
                },
            )
        return logged_user

    return role_checker


def get_logged_admin_user(
    logged_user: User = Depends(role_required([UserRole.ADMIN])),
) -> User:
    return logged_user


def get_logged_manager_user(
    logged_user: User = Depends(role_required([UserRole.MANAGER, UserRole.ADMIN])),
) -> User:
    return logged_user


def get_logged_viewer_user(
    logged_user: User = Depends(
        role_required([UserRole.MANAGER, UserRole.CUSTOMER, UserRole.ADMIN])
    ),
) -> User:
    return logged_user
