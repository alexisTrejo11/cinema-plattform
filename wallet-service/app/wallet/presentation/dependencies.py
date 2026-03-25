from app.config.postgres_config import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from app.wallet.infrastructure.persistence.sql.transaction_repository import (
    SqlAlchemyWalletTransactionRepository,
)
from app.wallet.infrastructure.persistence.sql.wallet_repository import (
    SqlAlchemyWalletRepository,
)
from app.wallet.application.use_cases.container import WalletUseCases
from app.user.presentation.dependencies import get_user_repository, UserRepository


def get_wallet_repository(
    session: AsyncSession = Depends(get_db),
) -> WalletRepository:
    return SqlAlchemyWalletRepository(session)


def get_wallet_transaction_repository(
    session: AsyncSession = Depends(get_db),
) -> WalletTransactionRepository:
    return SqlAlchemyWalletTransactionRepository(session)


def get_wallet_uc(
    wallet_repo: SqlAlchemyWalletRepository = Depends(get_wallet_repository),
    transaction_repo: WalletTransactionRepository = Depends(
        get_wallet_transaction_repository
    ),
    user_repo: UserRepository = Depends(get_user_repository),
) -> WalletUseCases:
    return WalletUseCases(wallet_repo, transaction_repo, user_repo)
