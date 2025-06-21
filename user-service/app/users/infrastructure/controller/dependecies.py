from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db
from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository
from app.auth.application.services import PasswordService, AuthValidationService
from app.users.application.use_cases import ListUsersUseCase, GetUserUseCase, CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase, BanUserUseCase

def get_user_repository(session: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)

def get_user_validation_service(repository: SQLAlchemyUserRepository = Depends(get_user_repository)) -> AuthValidationService:
    pw_service = PasswordService()
    return AuthValidationService(repository, pw_service)

def get_user_use_case(repository: SQLAlchemyUserRepository = Depends(get_user_repository))  -> GetUserUseCase:
    return GetUserUseCase(repository)

def list_user_use_case(repository: SQLAlchemyUserRepository = Depends(get_user_repository)) -> ListUsersUseCase:
    return ListUsersUseCase(repository)

def create_user_use_case(
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    validation_service: AuthValidationService = Depends(get_user_validation_service)
) -> CreateUserUseCase:
    pw_service = PasswordService()
    return CreateUserUseCase(repository, pw_service, validation_service)

def update_user_use_case(
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    validation_service: AuthValidationService = Depends(get_user_validation_service)
) -> UpdateUserUseCase:
    pw_service = PasswordService()
    return UpdateUserUseCase(repository, validation_service, pw_service)

def delete_user_use_case(session: AsyncSession = Depends(get_db)) -> DeleteUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    return DeleteUserUseCase(repository)


def ban_user_use_case(session: AsyncSession = Depends(get_db)) -> BanUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    return BanUserUseCase(repository)
