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


def get_user_by_id_uc(repo=Depends(get_db)) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)


def get_user_by_email_uc(repo=Depends(get_db)) -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase(repo)


def create_user_uc(repo=Depends(get_db)) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def update_user_uc(repo=Depends(get_db)) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


def delete_user_uc(repo=Depends(get_db)) -> SoftDeleteUserUseCase:
    return SoftDeleteUserUseCase(repo)


def list_users_uc(repo=Depends(get_db)) -> ListUsersUseCase:
    return ListUsersUseCase(repo)
