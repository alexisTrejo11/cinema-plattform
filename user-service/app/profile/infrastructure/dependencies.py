from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from app.profile.application.use_case import GetProfileUseCase, UpdateProfileUseCase
from app.users.infrastructure.persistence.sqlalch_user_repo import (
    SQLAlchemyUserRepository,
)


def get_profile_use_case() -> GetProfileUseCase:
    return GetProfileUseCase()


def update_profile_use_case(
    session: AsyncSession = Depends(get_db),
) -> UpdateProfileUseCase:
    repository = SQLAlchemyUserRepository(session)
    return UpdateProfileUseCase(repository)
