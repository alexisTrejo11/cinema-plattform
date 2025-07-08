from config.postgres_config import get_db
from fastapi import Depends
from app.infrastructure.persistence.wallet_repository import SQLAlchemyWalletRepository
from app.infrastructure.persistence.user_repository import SQLAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.use_cases.wallet_use_cases import WalletUseCases
from app.application.service.user_service import UserService


def get_wallet_repository(
    session: AsyncSession = Depends(get_db),
) -> SQLAlchemyWalletRepository:
    return SQLAlchemyWalletRepository(session)


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


def get_user_service(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_wallet_uc(
    repo: SQLAlchemyWalletRepository = Depends(get_wallet_repository),
) -> WalletUseCases:
    return WalletUseCases(repo)
