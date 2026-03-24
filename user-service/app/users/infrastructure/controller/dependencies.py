from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.app_config import settings
from config.postgres_config import get_db
from config.redis_config import get_redis_client

from app.auth.application.services import PasswordService, AuthValidationService
from app.token.application.repository import TokenRepository
from app.token.application.service import TokenService
from app.token.infrastructure.redis_repository import RedisTokenRepository
from app.token.infrastructure.services.token_service_impl import TokenServiceImpl
from app.users.application.container import UsersUseCasesContainer, build_users_use_cases
from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository


def get_token_repository(redis_conn=Depends(get_redis_client)) -> TokenRepository:
    return RedisTokenRepository(redis_conn)


def get_token_service(token_repo=Depends(get_token_repository)) -> TokenService:
    return TokenServiceImpl(token_repo, settings.SECRET_KEY, settings.ALGORITHM)


def get_user_repository(session: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


def get_password_service() -> PasswordService:
    return PasswordService()


def get_user_validation_service(
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenService = Depends(get_token_service),
) -> AuthValidationService:
    return AuthValidationService(repository, password_service, token_service)


def get_user_use_cases(
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    validation_service: AuthValidationService = Depends(get_user_validation_service),
    token_service: TokenService = Depends(get_token_service),
) -> UsersUseCasesContainer:
    return build_users_use_cases(
        repository=repository,
        password_service=password_service,
        validation_service=validation_service,
        token_service=token_service,
    )
