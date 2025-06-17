from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db
from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository
from app.auth.application.services import PasswordService, AuthValidationService
from app.users.application.use_cases import ( 
    ListUserUseCase, GetUserUseCase, CreateUserUseCase, 
    UpdateUserUseCase, DeleteUserUseCase, GetProfileUseCase,
    UpdateProfileUseCase
)

def get_user_use_case(session: AsyncSession = Depends(get_db))  -> GetUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    return GetUserUseCase(repository)

def list_user_use_case(session: AsyncSession = Depends(get_db)) -> ListUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    return ListUserUseCase(repository)

def create_user_use_case(session: AsyncSession = Depends(get_db)) -> CreateUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    pw_service = PasswordService()
    validation_service = AuthValidationService(repository, pw_service)
    return CreateUserUseCase(repository, pw_service, validation_service)

def update_user_use_case(session: AsyncSession = Depends(get_db)) -> UpdateUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    pw_service = PasswordService()
    validation_service = AuthValidationService(repository, pw_service)
    return UpdateUserUseCase(repository, validation_service, pw_service)

def delete_user_use_case(session: AsyncSession = Depends(get_db)) -> DeleteUserUseCase:
    repository = SQLAlchemyUserRepository(session)
    return DeleteUserUseCase(repository)


# Profile
def get_profile_use_case() -> GetProfileUseCase:
    return GetProfileUseCase()

def update_profile_use_case(session: AsyncSession = Depends(get_db)) -> UpdateProfileUseCase:
    repository = SQLAlchemyUserRepository(session)
    return UpdateProfileUseCase(repository)