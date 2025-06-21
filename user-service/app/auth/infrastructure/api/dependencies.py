from typing import List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config.postgres_config import get_db
from config.redis_config import get_redis_client, redis
from config.app_config import Settings, get_settings

from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User, UserRole

from app.token.application.repository import TokenRepository
from app.token.infrastructure.repository.token_repository import TokenRepositoryImpl 
from app.token.infrastructure.services.token_service_impl import TokenServiceImpl

from app.auth.application.usecases.signup_usecase import SignUpUseCase
from app.auth.application.usecases.login_usecase import  LoginUseCase, RefreshTokenUseCase
from app.auth.application.usecases.logout_usecase import LogoutAllUseCase, LogoutUseCase
from app.auth.application.services import TokenService, PasswordService, AuthValidationService, SessionService
from app.auth.domain.exceptions import InvalidCredentialsException

from app.notification.infrastructure.services_impl import NotificationServiceImpl
from app.notification.application.services import NotificationService

security = HTTPBearer()

# --- Repository Dependencies ---
def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)

def get_token_repository(redis_client: redis.Redis = Depends(get_redis_client)) -> TokenRepository:
    return TokenRepositoryImpl(redis_client)


# --- Service Dependencies ---
def get_password_service() -> PasswordService:
    return PasswordService()

def get_token_service(token_repo: TokenRepository = Depends(get_token_repository), settings: Settings = Depends(get_settings)) -> TokenService:
    """
    Dependency that provides an instance of TokenService,
    initialized with the secret key from your application settings.
    """
    return TokenServiceImpl(token_repository=token_repo, secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_auth_validation_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenService = Depends(get_token_service)
) -> AuthValidationService:
    """
    Provides an instance of AuthValidationService.
    """
    return AuthValidationService(user_repo, password_service, token_service)

def get_session_service(token_service: TokenService = Depends(get_token_service)) -> SessionService:
    """
    Provides an instance of SessionService.
    """
    return SessionService(token_service)

def get_notification_service() -> NotificationService:
    return NotificationServiceImpl()

# --- Use Case Dependencies ---
def signup_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    validation_service: AuthValidationService = Depends(get_auth_validation_service)
) -> SignUpUseCase:
    """
    Provides an instance of SignUpUseCase.
    """
    return SignUpUseCase(user_repo, validation_service, password_service)

def login_use_case(
    session_service: SessionService = Depends(get_session_service),
    token_service: TokenService = Depends(get_token_service),
    validation_service: AuthValidationService = Depends(get_auth_validation_service),
    notification_service : NotificationService = Depends(get_notification_service)
) -> LoginUseCase:
    """
    Provides an instance of LoginUseCase.
    """
    return LoginUseCase(session_service, validation_service, token_service, notification_service)

def logout_use_case(
    session_service: SessionService = Depends(get_session_service)
) -> LogoutUseCase:
    """
    Provides an instance of LogoutUseCase.
    """
    return LogoutUseCase(session_service)

def logout_all_use_case(
    session_service: SessionService = Depends(get_session_service)
) -> LogoutAllUseCase:
    """
    Provides an instance of LogoutAllUseCase.
    """
    return LogoutAllUseCase(session_service)

def refresh_token_use_case(
    session_service: SessionService = Depends(get_session_service)
) -> RefreshTokenUseCase:
    """
    Provides an instance of RefreshTokenUseCase.
    """
    return RefreshTokenUseCase(session_service)


# --- User Authorization Dependency ---
async def get_logged_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> User:
    try:
        payload = token_service.verify_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = await user_repository.get_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except InvalidCredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or credentials")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authentication error: {e}")


def role_required(required_roles: List[UserRole]) -> Callable[[User], User]:
    """
    Dependency factory to check if the current user has any of the specified roles.
    """
    def role_checker(logged_user: User = Depends(get_logged_user)) -> User:
        if logged_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required roles: {[r.value for r in required_roles]}"
            )
        return logged_user
    return role_checker


def get_logged_admin_user(logged_user: User = Depends(role_required([UserRole.ADMIN]))) -> User:
    return logged_user

def get_logged_manager_user(logged_user: User = Depends(role_required([UserRole.MANAGER, UserRole.ADMIN]))) -> User:
    return logged_user

def get_logged_viewer_user(logged_user: User = Depends(role_required([UserRole.MANAGER, UserRole.CUSTOMER, UserRole.ADMIN]))) -> User:
    return logged_user
