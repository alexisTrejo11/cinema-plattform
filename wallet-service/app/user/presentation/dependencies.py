from fastapi import Depends
from app.user.application.usecases import (
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    ListUsersUseCase,
    CreateUserUseCase,
    UpdateUserUseCase,
    SoftDeleteUserUseCase,
)
from config.postgres_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.infrastructure.sql_user_respository import SqlAlchemyUserRepository
from app.user.domain.repository import UserRepository


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_user_by_id_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)


def get_user_by_email_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase(repo)


def create_user_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def update_user_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


def delete_user_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> SoftDeleteUserUseCase:
    return SoftDeleteUserUseCase(repo)


def list_users_uc(
    repo: UserRepository = Depends(get_user_repository),
) -> ListUsersUseCase:
    return ListUsersUseCase(repo)
