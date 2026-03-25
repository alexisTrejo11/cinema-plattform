from ast import Tuple
import asyncio

from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.interfaces import (
    WalletRepository,
    WalletTransactionRepository,
    WalletEventPublisher,
    UserInternalService,
    TransactionEvents,
)
from app.wallet.domain.entities import User
from app.wallet.domain.exceptions import UserNotFoundError, UserWalletConflict
from app.wallet.domain.value_objects import UserId

from ..commands import (
    AddCreditCommand,
    CreateWalletCommand,
    PayWithWalletCommand,
)


class InitWalletForUserUseCase:
    def __init__(
        self, wallet_repo: WalletRepository, user_service: UserInternalService
    ):
        self.wallet_repo = wallet_repo
        self.user_service = user_service

    async def execute(self, command: CreateWalletCommand) -> UserInternalService:
        """Creates a new wallet for a user."""
        await self._validate(command.user_id)
        return await self._proces_creation(command)

    async def _proces_creation(self, command: CreateWalletCommand) -> Wallet:
        new_wallet = Wallet.create(command.user_id)
        created_wallet = await self.wallet_repo.create(new_wallet)
        return Wallet.from_domain(created_wallet)

    async def _validate(self, user_id: UserId) -> None:
        user = await self.user_service.get_by_id(user_id.to_string())
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

    async def execute(
        self, command: AddCreditCommand
    ) -> Tuple[Wallet, WalletTransaction]:
        """Adds credit to a wallet."""
        wallet = await self.wallet_repo.get_by_id(
            command.wallet_id, raise_exception=True
        )
        transaction = wallet.buy_credit(command.payment_details, command.amount)

        buy_coroutine = self._proccess_buy(wallet, transaction)
        event_couroutine = self.event_publisher.publish_event(
            wallet, transaction, TransactionEvents.CHARGE_CREDIT
        )

        wallet_updated, transaction_created = await asyncio.gather(
            buy_coroutine, event_couroutine
        )
        return wallet_updated, transaction_created

    async def _proccess_buy(
        self, wallet: Wallet, transaction: WalletTransaction
    ) -> Tuple[Wallet, WalletTransaction]:
        wallet_updated = await self.wallet_repo.update(wallet)
        transaction_created = await self.transaction_repo.create(transaction)

        return wallet_updated, transaction_created


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

    async def execute(
        self, command: PayWithWalletCommand
    ) -> Tuple[Wallet, WalletTransaction]:
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
    ) -> Tuple[Wallet, WalletTransaction]:
        wallet_updated = await self.wallet_repo.update(wallet)
        transaction_created = await self.transaction_repo.create(transaction)

        return wallet_updated, transaction_created
