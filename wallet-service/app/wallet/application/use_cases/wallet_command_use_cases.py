import logging

from app.wallet.application.commands import (
    AddCreditCommand,
    CreateWalletCommand,
    PayWithWalletCommand,
)
from app.wallet.domain.entities import Wallet
from app.wallet.domain.interfaces import (
    TransactionEvents,
    UserInternalService,
    WalletEventPublisher,
    WalletRepository,
    WalletTransactionRepository,
    PaymentInternalService,
)
from app.wallet.domain.exceptions import (
    UserNotFoundError,
    UserWalletConflict,
    WalletNotFoundError,
    PaymentFailedError,
)
from app.wallet.application.results import WalletOperationOutcome
from app.wallet.domain.value_objects import UserId, WalletId

logger = logging.getLogger(__name__)


class InitWalletForUserUseCase:
    """
    Use case for initializing a wallet for a user.
    Normally this use case will be occur when a new user is created.
    """

    def __init__(
        self,
        wallet_repo: WalletRepository,
        user_service: UserInternalService,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._user_service = user_service

    async def execute(self, command: CreateWalletCommand) -> Wallet:
        """
        Creates a wallet for a user.

        Args:
            command: The command for the wallet.
        Returns:
            The wallet.
        Raises:
            UserNotFoundError: If the user is not found.
            UserWalletConflict: If the user already has a wallet.
        """
        logger.info("Creating wallet for user_id=%s", command.user_id.value)
        await self._validate_user(command.user_id)

        new_wallet = Wallet.create(command.user_id)
        created = await self._wallet_repo.create(new_wallet)

        logger.info(
            "Wallet created wallet_id=%s user_id=%s",
            created.id.value,
            command.user_id.value,
        )
        return created

    async def _validate_user(self, user_id: UserId) -> None:
        user = await self._user_service.get_user_details(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        if await self._wallet_repo.exists_by_user_id(user_id):
            raise UserWalletConflict("User already has a wallet")


class AddCreditUseCase:
    """
    Use case for adding credit to a wallet.
    IMPORTANT: This use case also acts as an orchestrator for the payment process.
    """

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo
        self._event_publisher = event_publisher

    async def execute(self, command: AddCreditCommand) -> WalletOperationOutcome:
        """
        Performs a credit transaction on a wallet.

        Args:
            command: The command for the credit.
        Returns:
            Updated wallet and persisted transaction.
        Raises:
            WalletNotFoundError: If the wallet is not found.
        """
        await self._validate_wallet(command.wallet_id)
        wallet = await self._wallet_repo.find_by_id(command.wallet_id)
        if not wallet:
            raise WalletNotFoundError(command.wallet_id)

        transaction = wallet.buy_credit(command.payment_details, command.amount)

        # TODO: Add output data of payment to the transaction. Validate input data of payment.
        payment_result = await self._payment_service.create_payment(
            command.payment_details
        )
        if not payment_result.is_success():
            raise PaymentFailedError(payment_result.error())

        wallet_updated = await self._wallet_repo.update(wallet)
        transaction_created = await self._transaction_repo.create(transaction)

        await self._event_publisher.publish_event(
            wallet_updated,
            transaction_created,
            TransactionEvents.CHARGE_CREDIT,
        )

        logger.info(
            "Add-credit flow completed wallet_id=%s",
            command.wallet_id.value,
        )

        return WalletOperationOutcome(
            wallet=wallet_updated, transaction=transaction_created
        )


class PayWithWalletUseCase:
    """
    Use case for paying with a wallet.
    IMPORTANT: This use case also acts as an orchestrator for the payment process.
    """

    def __init__(
        self,
        payment_service: PaymentInternalService,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
        event_publisher: WalletEventPublisher,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo
        self._event_publisher = event_publisher
        self._payment_service = payment_service

    async def execute(self, cmd: PayWithWalletCommand) -> WalletOperationOutcome:
        """
        Pay with a wallet.

        Args:
            cmd: The cmd for the payment.
        Returns:
            Updated wallet and persisted transaction.
        Raises:
            WalletNotFoundError: If the wallet is not found.
        """
        wallet = await self._wallet_repo.find_by_id(cmd.wallet_id)
        if not wallet:
            raise WalletNotFoundError(cmd.wallet_id)

        # TODO: Add output data of payment to the transaction
        payment_result = await self._payment_service.create_payment(cmd.payment_details)
        if not payment_result.is_success():
            raise PaymentFailedError(payment_result.error())

        transaction = wallet.buy_product(cmd.payment_details, cmd.charge)

        transaction_created = await self._transaction_repo.create(transaction)
        wallet_updated = await self._wallet_repo.update(wallet)

        await self._event_publisher.publish_event(
            wallet_updated,
            transaction_created,
            TransactionEvents.BUY_PRODUCT,
        )

        logger.info(
            "Pay flow completed wallet_id=%s",
            cmd.wallet_id.value,
        )

        return WalletOperationOutcome(
            wallet=wallet_updated, transaction=transaction_created
        )


class DeleteWalletUseCase:
    """
    Use case for deleting a wallet.
    This should occur when a user is deleted.
    """

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo

    async def execute(self, wallet_id: WalletId) -> Wallet:
        wallet = await self._wallet_repo.find_by_id(wallet_id)
        if not wallet:
            raise WalletNotFoundError(wallet_id)

        await self._wallet_repo.delete(wallet)
        return wallet


class RestoreWalletUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo

    async def execute(self, wallet_id) -> Wallet:
        wallet = await self._wallet_repo.find_by_id(
            wallet_id, include_transactions=True
        )
        if not wallet:
            raise WalletNotFoundError(wallet_id)

        wallet.restore()

        await self._wallet_repo.update(wallet)
        return wallet
