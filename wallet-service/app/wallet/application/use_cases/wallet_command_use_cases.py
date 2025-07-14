from typing import Optional, List
import asyncio
from uuid import UUID
from app.user.domain.value_objects import UserId
from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
    WalletTransaction,
)

from app.wallet.domain.enums import TransactionType
from ..dtos.wallet_dtos import (
    AddCreditCommand,
    PayResponse,
    CreateWalletCommand,
    WalletBuyResponse,
    BuyCreditResponse,
    PayWithWalletCommand,
)


class InitWalletForUserUseCase:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, command: CreateWalletCommand) -> BuyCreditResponse:
        """Creates a new wallet for a user."""
        user_id = UserId(command.user_id.value)
        new_wallet = Wallet.create(user_id)

        created_wallet = await self.wallet_repo.create(new_wallet)
        return BuyCreditResponse.model_validate(created_wallet)


class AddCreditUseCase:
    """Use case for adding credit to a wallet. Produces a Transaction"""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    async def execute(self, command: AddCreditCommand) -> BuyCreditResponse:
        """Adds credit to a wallet."""
        wallet = await self.wallet_repo.get_by_id(command.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        transaction = wallet.add_credit(
            command.amount, TransactionType.BUY_PRODUCT, command.payment_details
        )

        return await self._proccess_buy(wallet, transaction)

    async def _proccess_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> BuyCreditResponse:
        event_couroutine = self._publish_event(wallet, transaction)
        wallet_couroutine = self.wallet_repo.update(wallet)
        transaction_couroutine = self.transaction_repo.create(transaction)

        _, wallet_updated, transaction_created = await asyncio.gather(
            event_couroutine, wallet_couroutine, transaction_couroutine
        )

        return BuyCreditResponse(
            id=wallet_updated.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount,
            transaction=transaction_created.__dict__,
        )

    async def _publish_event(self, wallet: Wallet, transaction: WalletTransaction):
        # Produce RabbitMQ message to notification service
        pass


class PayWithWalletUseCase:
    """Use case for making a payment from a wallet.  Produces a Transaction"""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    async def execute(self, command: PayWithWalletCommand) -> WalletBuyResponse:
        """Makes a payment from a wallet."""
        wallet = await self.wallet_repo.get_by_id(command.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        transaction = wallet.remove_credit(
            command.payment_details, command.amount, TransactionType.BUY_PRODUCT
        )

        return await self._proccess_buy(wallet, transaction)

    async def _proccess_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> WalletBuyResponse:
        event_couroutine = self._publish_event(wallet, transaction)
        wallet_couroutine = self.wallet_repo.update(wallet)
        transaction_couroutine = self.transaction_repo.create(transaction)

        _, wallet_updated, transaction_created = await asyncio.gather(
            event_couroutine, wallet_couroutine, transaction_couroutine
        )

        return WalletBuyResponse(
            id=wallet_updated.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount,
            transaction=transaction_created.__dict__,
        )

    async def _publish_event(self, wallet: Wallet, transaction: WalletTransaction):
        # Produce RabbitMQ message to notification service
        pass
