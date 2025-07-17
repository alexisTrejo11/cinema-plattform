import asyncio
from app.user.domain.value_objects import UserId
from app.user.domain.repository import UserRepository

from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from app.wallet.presentation.dtos.response import WalletBuyResponse, WalletResponse

from ...event_publisher import WalletEventPublisher, TransactionEvents
from ...exceptions import UserNotFoundError, UserWalletConflict
from ...command.commands import (
    AddCreditCommand,
    CreateWalletCommand,
    PayWithWalletCommand,
)


class InitWalletForUserUseCase:
    def __init__(self, wallet_repo: WalletRepository, user_repo: UserRepository):
        self.wallet_repo = wallet_repo
        self.user_repo = user_repo

    async def execute(self, command: CreateWalletCommand) -> WalletResponse:
        """Creates a new wallet for a user."""
        await self._validate(command.user_id)
        return await self._proces_creation(command)

    async def _proces_creation(self, command: CreateWalletCommand) -> WalletResponse:
        new_wallet = Wallet.create(command.user_id)
        created_wallet = await self.wallet_repo.create(new_wallet)
        return WalletResponse.from_domain(created_wallet)

    async def _validate(self, user_id: UserId) -> None:
        user = await self.user_repo.get_by_id(user_id.to_string())
        if not user:
            raise UserNotFoundError(user_id)

        user_wallet = await self.wallet_repo.get_by_user_id(user_id)
        if user_wallet:
            raise UserWalletConflict("User Already Has a Wallet")


class AddCreditUseCase:
    """Use case for adding credit to a wallet. Produces a Transaction"""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo
        self.event_publisher = event_publisher

    async def execute(self, command: AddCreditCommand) -> WalletBuyResponse:
        """Adds credit to a wallet."""
        wallet = await self.wallet_repo.get_by_id(
            command.wallet_id, raise_exception=True
        )
        transaction = wallet.buy_credit(command.payment_details, command.amount)

        buy_coroutine = self._proccess_buy(wallet, transaction)
        event_couroutine = self.event_publisher.publish_event(
            wallet, transaction, TransactionEvents.CHARGE_CREDIT
        )

        response, _ = await asyncio.gather(buy_coroutine, event_couroutine)
        return response

    async def _proccess_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> WalletBuyResponse:
        wallet_updated = await self.wallet_repo.update(wallet)
        transaction_created = await self.transaction_repo.create(transaction)

        return WalletBuyResponse.from_domain(wallet_updated, transaction_created)


class PayWithWalletUseCase:
    """Use case for making a payment from a wallet.  Produces a Transaction"""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo
        self.event_publisher = event_publisher

    async def execute(self, command: PayWithWalletCommand) -> WalletBuyResponse:
        """Makes a payment from a wallet."""
        wallet = await self.wallet_repo.get_by_id(
            command.wallet_id, raise_exception=True
        )

        transaction = wallet.buy_product(command.payment_details, command.charge)

        buy_coroutine = self._proccess_buy(wallet, transaction)
        event_couroutine = self.event_publisher.publish_event(
            wallet, transaction, TransactionEvents.CHARGE_CREDIT
        )

        response, _ = await asyncio.gather(buy_coroutine, event_couroutine)
        return response

    async def _proccess_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> WalletBuyResponse:
        wallet_updated = await self.wallet_repo.update(wallet)
        transaction_created = await self.transaction_repo.create(transaction)

        return WalletBuyResponse.from_domain(wallet_updated, transaction_created)
