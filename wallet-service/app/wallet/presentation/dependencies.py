from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.app_config import settings
from app.config.postgres_config import get_db
from app.wallet.application.use_cases.container import (
    WalletUseCases,
)  # noqa: F401 — re-export for controllers
from app.wallet.domain.interfaces import (
    UserInternalService,
    WalletEventPublisher,
    WalletRepository,
    WalletTransactionRepository,
)
from app.wallet.infrastructure.message.noop_wallet_event_publisher import (
    NoOpWalletEventPublisher,
)
from app.wallet.infrastructure.message.wallet_producer import (
    build_wallet_event_producer,
)
from app.wallet.infrastructure.persistence.sql.transaction_repository import (
    SqlAlchemyWalletTransactionRepository,
)
from app.wallet.infrastructure.persistence.sql.wallet_repository import (
    SqlAlchemyWalletRepository,
)


def get_wallet_repository(
    session: AsyncSession = Depends(get_db),
) -> WalletRepository:
    return SqlAlchemyWalletRepository(session)


def get_wallet_transaction_repository(
    session: AsyncSession = Depends(get_db),
) -> WalletTransactionRepository:
    return SqlAlchemyWalletTransactionRepository(session)


def get_wallet_event_publisher() -> WalletEventPublisher:
    if not settings.KAFKA_ENABLED:
        return NoOpWalletEventPublisher()
    return build_wallet_event_producer()


def get_wallet_uc(
    wallet_repo: WalletRepository = Depends(get_wallet_repository),
    transaction_repo: WalletTransactionRepository = Depends(
        get_wallet_transaction_repository
    ),
    # TODO: Implement user service
    user_service: UserInternalService = Depends(),
    event_publisher: WalletEventPublisher = Depends(get_wallet_event_publisher),
) -> WalletUseCases:
    return WalletUseCases(
        wallet_repo,
        transaction_repo,
        user_service,
        event_publisher,
    )
