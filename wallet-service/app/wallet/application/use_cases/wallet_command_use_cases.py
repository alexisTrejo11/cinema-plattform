from __future__ import annotations

from app.wallet.application.commands import (
    AddCreditCommand,
    CreateWalletCommand,
    PayWithWalletCommand,
)
from app.wallet.domain.entities import Wallet
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.interfaces import (
    TransactionEvents,
    UserInternalService,
    WalletEventPublisher,
    WalletRepository,
    WalletTransactionRepository,
)
from app.wallet.domain.exceptions import UserNotFoundError, UserWalletConflict
from app.wallet.presentation.dtos.response import WalletBuyResponse, WalletResponse


class InitWalletForUserUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        user_service: UserInternalService,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._user_service = user_service

    async def execute(self, command: CreateWalletCommand) -> WalletResponse:
        user = await self._user_service.get_user_details(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id.to_string())

        existing = await self._wallet_repo.get_by_user_id(command.user_id)
        if existing:
            raise UserWalletConflict("User already has a wallet")

        new_wallet = Wallet.create(command.user_id)
        created = await self._wallet_repo.create(new_wallet)
        return WalletResponse.from_domain(created)


class AddCreditUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo
        self._event_publisher = event_publisher

    async def execute(self, command: AddCreditCommand) -> WalletBuyResponse:
        wallet = await self._wallet_repo.get_by_id(
            command.wallet_id,
            raise_exception=True,
        )
        transaction = wallet.buy_credit(command.payment_details, command.amount)

        wallet_updated, transaction_created = await self._process_buy(
            wallet, transaction
        )
        await self._event_publisher.publish_event(
            wallet_updated,
            transaction_created,
            TransactionEvents.CHARGE_CREDIT,
        )
        return WalletBuyResponse.from_domain(wallet_updated, transaction_created)

    async def _process_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> tuple[Wallet, WalletTransaction]:
        wallet_updated = await self._wallet_repo.update(wallet)
        transaction_created = await self._transaction_repo.create(transaction)
        return wallet_updated, transaction_created


class PayWithWalletUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo
        self._event_publisher = event_publisher

    async def execute(self, command: PayWithWalletCommand) -> WalletBuyResponse:
        wallet = await self._wallet_repo.get_by_id(
            command.wallet_id,
            raise_exception=True,
        )
        transaction = wallet.buy_product(command.payment_details, command.charge)

        wallet_updated, transaction_created = await self._process_buy(
            wallet, transaction
        )
        await self._event_publisher.publish_event(
            wallet_updated,
            transaction_created,
            TransactionEvents.BUY_PRODUCT,
        )
        return WalletBuyResponse.from_domain(wallet_updated, transaction_created)

    async def _process_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> tuple[Wallet, WalletTransaction]:
        wallet_updated = await self._wallet_repo.update(wallet)
        transaction_created = await self._transaction_repo.create(transaction)
        return wallet_updated, transaction_created
