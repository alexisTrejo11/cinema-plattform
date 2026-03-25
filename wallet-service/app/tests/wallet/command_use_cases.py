import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import uuid
from datetime import datetime, timezone
from decimal import Decimal

# Import domain entities and value objects
from app.user.domain.user import User  # Assuming User domain entity
from app.user.domain.value_objects import UserId
from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.value_objects import WalletId, Money, Charge, PaymentDetails
from app.wallet.domain.enums import Currency, TransactionType

# Import repositories (interfaces)
from app.user.domain.repository import UserRepository
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)

# Import use cases (Adjust paths if necessary based on your structure)
from app.wallet.application.use_cases.wallet.wallet_command_use_cases import (
    InitWalletForUserUseCase,
    AddCreditUseCase,
    PayWithWalletUseCase,
)

# Import event publisher and events
from app.wallet.application.event_publisher import (
    WalletEventPublisher,
    TransactionEvents,
)

# Import DTOs and Commands
from app.wallet.presentation.dtos.response import WalletResponse, WalletBuyResponse
from app.wallet.application.command.commands import (
    AddCreditCommand,
    CreateWalletCommand,
    PayWithWalletCommand,
)

# Import Exceptions
from app.wallet.application.exceptions import (
    UserNotFoundError,
    UserWalletConflict,
    WalletNotFoundError,
)

# from app.user.domain.exceptions import UserNotFoundException # If this is explicitly raised, import it


# --- Fixtures for Mocks and Dummy Data ---


@pytest.fixture
def mock_wallet_repo():
    """Mocks WalletRepository using AsyncMock."""
    return AsyncMock(spec=WalletRepository)


@pytest.fixture
def mock_user_repo():
    """Mocks UserRepository using AsyncMock."""
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def mock_transaction_repo():
    """Mocks WalletTransactionRepository using AsyncMock."""
    return AsyncMock(spec=WalletTransactionRepository)


@pytest.fixture
def mock_event_publisher():
    """Mocks WalletEventPublisher using AsyncMock.
    Ensures publish_event returns an awaitable AsyncMock method.
    """
    publisher = AsyncMock(spec=WalletEventPublisher)
    # The default behavior of AsyncMock methods is to return awaitable Mocks.
    # We explicitly ensure it by re-assigning it to an AsyncMock if needed,
    # or just let the default behavior work for 'publish_event'.
    # For asyncio.gather to work well with mocks, ensure the mock's method
    # itself is an awaitable or returns an awaitable. AsyncMock usually handles this.
    # If the RuntimeError persists, consider:
    # publisher.publish_event.return_value = asyncio.Future()
    # Or a simple awaitable mock:
    publisher.publish_event = AsyncMock()
    return publisher


@pytest.fixture
def dummy_user_id() -> UserId:
    return UserId(uuid.uuid4())


@pytest.fixture
def dummy_wallet_id() -> WalletId:
    return WalletId(value=uuid.uuid4())


@pytest.fixture
def dummy_user_domain(dummy_user_id: UserId) -> User:
    """Provides a dummy User domain object."""
    user = MagicMock(spec=User)
    # Mock the get_id method to return a UserId object with to_string method
    mock_user_id = MagicMock(spec=UserId)
    mock_user_id.value = dummy_user_id.value
    mock_user_id.to_string.return_value = str(dummy_user_id.value)
    user.get_id.return_value = mock_user_id
    return user


@pytest.fixture
def dummy_transaction_domain(dummy_wallet_id: WalletId) -> WalletTransaction:
    """Provides a dummy WalletTransaction domain object."""
    transaction = MagicMock(spec=WalletTransaction)
    transaction.id = WalletId(value=uuid.uuid4())
    transaction.wallet_id = dummy_wallet_id
    transaction.amount = Money(amount=Decimal("10.00"), currency=Currency.USD)
    transaction.type = TransactionType.ADD_CREDIT
    transaction.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    transaction.payment_details = MagicMock(spec=PaymentDetails)
    return transaction


@pytest.fixture
def dummy_wallet_domain(
    dummy_wallet_id: WalletId,
    dummy_user_id: UserId,
    dummy_transaction_domain: WalletTransaction,
) -> Wallet:
    """Provides a dummy Wallet domain object with mocked methods for interactions."""
    wallet = MagicMock(spec=Wallet)
    wallet.id = dummy_wallet_id  # Use property directly
    wallet.user_id = dummy_user_id  # Use property directly
    wallet.balance = Money(amount=Decimal("100.00"), currency=Currency.USD)
    wallet.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    wallet.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    wallet.transactions = []

    # Mock domain methods that use cases call to return the specific dummy transaction
    wallet.buy_credit.return_value = dummy_transaction_domain
    wallet.buy_product.return_value = dummy_transaction_domain

    return wallet


@pytest.fixture
def mock_wallet_response_from_domain():
    with patch(
        "app.wallet.presentation.dtos.response.WalletResponse.from_domain"
    ) as mock:
        mock_response = MagicMock(spec=WalletResponse)
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def mock_wallet_buy_response_from_domain():
    with patch(
        "app.wallet.presentation.dtos.response.WalletBuyResponse.from_domain"
    ) as mock:
        mock_response = MagicMock(spec=WalletBuyResponse)
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def dummy_payment_details() -> PaymentDetails:
    return MagicMock(spec=PaymentDetails)


class TestInitWalletForUserUseCase:

    @pytest.fixture
    def use_case(self, mock_wallet_repo, mock_user_repo):
        return InitWalletForUserUseCase(mock_wallet_repo, mock_user_repo)

    @pytest.fixture
    def create_wallet_command(self, dummy_user_id: UserId) -> CreateWalletCommand:
        return CreateWalletCommand(user_id=dummy_user_id)

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        use_case: InitWalletForUserUseCase,
        mock_wallet_repo: AsyncMock,
        mock_user_repo: AsyncMock,
        mock_wallet_response_from_domain: MagicMock,
        dummy_user_id: UserId,
        dummy_user_domain: User,
        dummy_wallet_domain: Wallet,
        create_wallet_command: CreateWalletCommand,
    ):
        """Tests successful wallet initialization for a new user."""
        # Arrange
        mock_user_repo.get_by_id.return_value = dummy_user_domain  # User exists
        mock_wallet_repo.get_by_user_id.return_value = None  # No existing wallet

        # Patch the static method Wallet.create
        with patch(
            "app.wallet.domain.entities.wallet.Wallet.create"
        ) as mock_wallet_create:
            mock_wallet_create.return_value = (
                dummy_wallet_domain  # Wallet.create returns a new wallet
            )
            mock_wallet_repo.create.return_value = (
                dummy_wallet_domain  # Repository creates it
            )

            # Act
            response = await use_case.execute(create_wallet_command)

            # Assert
            mock_user_repo.get_by_id.assert_called_once_with(
                create_wallet_command.user_id.to_string()
            )
            mock_wallet_repo.get_by_user_id.assert_called_once_with(
                create_wallet_command.user_id
            )
            mock_wallet_create.assert_called_once_with(
                create_wallet_command.user_id
            )  # Assert Wallet.create call
            mock_wallet_repo.create.assert_called_once_with(
                mock_wallet_create.return_value
            )
            mock_wallet_response_from_domain.assert_called_once_with(
                dummy_wallet_domain
            )
            assert response == mock_wallet_response_from_domain.return_value

    @pytest.mark.asyncio
    async def test_execute_user_not_found(
        self,
        use_case: InitWalletForUserUseCase,
        mock_user_repo: AsyncMock,
        mock_wallet_repo: AsyncMock,
        create_wallet_command: CreateWalletCommand,
    ):
        """Tests that UserNotFoundError is raised if user does not exist."""
        # Arrange
        mock_user_repo.get_by_id.return_value = None  # User not found

        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            await use_case.execute(create_wallet_command)

        mock_user_repo.get_by_id.assert_called_once_with(
            create_wallet_command.user_id.to_string()
        )
        mock_wallet_repo.get_by_user_id.assert_not_called()  # Should not proceed to check for existing wallet
        mock_wallet_repo.create.assert_not_called()
        assert str(create_wallet_command.user_id) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_user_wallet_conflict(
        self,
        use_case: InitWalletForUserUseCase,
        mock_user_repo: AsyncMock,
        mock_wallet_repo: AsyncMock,
        dummy_user_domain: User,
        dummy_wallet_domain: Wallet,
        create_wallet_command: CreateWalletCommand,
    ):
        """Tests that UserWalletConflict is raised if user already has a wallet."""
        # Arrange
        mock_user_repo.get_by_id.return_value = dummy_user_domain  # User exists
        mock_wallet_repo.get_by_user_id.return_value = (
            dummy_wallet_domain  # User already has a wallet
        )

        # Act & Assert
        with pytest.raises(UserWalletConflict) as exc_info:
            await use_case.execute(create_wallet_command)

        mock_user_repo.get_by_id.assert_called_once_with(
            create_wallet_command.user_id.to_string()
        )
        mock_wallet_repo.get_by_user_id.assert_called_once_with(
            create_wallet_command.user_id
        )
        mock_wallet_repo.create.assert_not_called()  # Should not attempt to create new wallet
        assert "Validation failed for field 'User" in str(exc_info.value)


class TestAddCreditUseCase:

    @pytest.fixture
    def use_case(self, mock_wallet_repo, mock_transaction_repo, mock_event_publisher):
        return AddCreditUseCase(
            mock_wallet_repo, mock_transaction_repo, mock_event_publisher
        )

    @pytest.fixture
    def add_credit_command(
        self, dummy_wallet_id: WalletId, dummy_payment_details: PaymentDetails
    ) -> AddCreditCommand:
        return AddCreditCommand(
            wallet_id=dummy_wallet_id,
            amount=Money(amount=Decimal("50.00"), currency=Currency.USD),
            payment_details=dummy_payment_details,
        )

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        use_case: AddCreditUseCase,
        mock_wallet_repo: AsyncMock,
        mock_transaction_repo: AsyncMock,  # Added as argument
        mock_event_publisher: AsyncMock,  # Added as argument
        mock_wallet_buy_response_from_domain: MagicMock,
        dummy_wallet_id: WalletId,
        dummy_wallet_domain: Wallet,
        dummy_transaction_domain: WalletTransaction,
        add_credit_command: AddCreditCommand,
    ):
        """Tests successful addition of credit to a wallet."""
        # Arrange
        mock_wallet_repo.get_by_id.return_value = dummy_wallet_domain
        # Mock the wallet's buy_credit method to return a transaction
        dummy_wallet_domain.buy_credit.return_value = dummy_transaction_domain
        mock_wallet_repo.update.return_value = dummy_wallet_domain  # Wallet updated
        mock_transaction_repo.create.return_value = (
            dummy_transaction_domain  # Transaction created
        )

        # Act
        response = await use_case.execute(add_credit_command)

        # Assert
        mock_wallet_repo.get_by_id.assert_called_once_with(
            add_credit_command.wallet_id, raise_exception=True
        )
        dummy_wallet_domain.buy_credit.assert_called_once_with(
            add_credit_command.payment_details, add_credit_command.amount
        )
        mock_wallet_repo.update.assert_called_once_with(dummy_wallet_domain)
        mock_transaction_repo.create.assert_called_once_with(dummy_transaction_domain)
        mock_wallet_buy_response_from_domain.assert_called_once_with(
            dummy_wallet_domain, dummy_transaction_domain
        )
        mock_event_publisher.publish_event.assert_called_once_with(
            dummy_wallet_domain,
            dummy_transaction_domain,
            TransactionEvents.CHARGE_CREDIT,  # Pass Enum member
        )
        assert response == mock_wallet_buy_response_from_domain.return_value

    @pytest.mark.asyncio
    async def test_execute_wallet_not_found(
        self,
        use_case: AddCreditUseCase,
        mock_wallet_repo: AsyncMock,
        mock_transaction_repo: AsyncMock,  # Added as argument
        mock_event_publisher: AsyncMock,  # Added as argument
        add_credit_command: AddCreditCommand,
    ):
        """Tests that WalletNotFoundError is raised if wallet does not exist."""
        # Arrange
        mock_wallet_repo.get_by_id.side_effect = WalletNotFoundError(
            str(add_credit_command.wallet_id)
        )

        # Act & Assert
        with pytest.raises(WalletNotFoundError) as exc_info:
            await use_case.execute(add_credit_command)

        mock_wallet_repo.get_by_id.assert_called_once_with(
            add_credit_command.wallet_id, raise_exception=True
        )
        # Ensure no further calls if wallet not found
        mock_transaction_repo.create.assert_not_called()
        mock_event_publisher.publish_event.assert_not_called()
        assert str(add_credit_command.wallet_id) in str(exc_info.value)


class TestPayWithWalletUseCase:

    @pytest.fixture
    def use_case(self, mock_wallet_repo, mock_transaction_repo, mock_event_publisher):
        return PayWithWalletUseCase(
            mock_wallet_repo, mock_transaction_repo, mock_event_publisher
        )

    @pytest.fixture
    def pay_with_wallet_command(
        self, dummy_wallet_id: WalletId, dummy_payment_details: PaymentDetails
    ) -> PayWithWalletCommand:
        return PayWithWalletCommand(
            wallet_id=dummy_wallet_id,
            charge=Charge(amount=Decimal("25.00"), currency=Currency.USD),
            payment_details=dummy_payment_details,
        )

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        use_case: PayWithWalletUseCase,
        mock_wallet_repo: AsyncMock,
        mock_transaction_repo: AsyncMock,  # Added as argument
        mock_event_publisher: AsyncMock,  # Added as argument
        mock_wallet_buy_response_from_domain: MagicMock,
        dummy_wallet_id: WalletId,
        dummy_wallet_domain: Wallet,
        dummy_transaction_domain: WalletTransaction,
        pay_with_wallet_command: PayWithWalletCommand,
    ):
        """Tests successful payment from a wallet."""
        # Arrange
        mock_wallet_repo.get_by_id.return_value = dummy_wallet_domain
        # Mock the wallet's buy_product method to return a transaction
        dummy_wallet_domain.buy_product.return_value = dummy_transaction_domain
        mock_wallet_repo.update.return_value = dummy_wallet_domain  # Wallet updated
        mock_transaction_repo.create.return_value = (
            dummy_transaction_domain  # Transaction created
        )

        # Act
        response = await use_case.execute(pay_with_wallet_command)

        # Assert
        mock_wallet_repo.get_by_id.assert_called_once_with(
            pay_with_wallet_command.wallet_id, raise_exception=True
        )
        dummy_wallet_domain.buy_product.assert_called_once_with(
            pay_with_wallet_command.payment_details, pay_with_wallet_command.charge
        )
        mock_wallet_repo.update.assert_called_once_with(dummy_wallet_domain)
        mock_transaction_repo.create.assert_called_once_with(dummy_transaction_domain)
        mock_wallet_buy_response_from_domain.assert_called_once_with(
            dummy_wallet_domain, dummy_transaction_domain
        )
        mock_event_publisher.publish_event.assert_called_once_with(
            dummy_wallet_domain,
            dummy_transaction_domain,
            TransactionEvents.CHARGE_CREDIT,  # Pass Enum member
        )
        assert response == mock_wallet_buy_response_from_domain.return_value

    @pytest.mark.asyncio
    async def test_execute_wallet_not_found(
        self,
        use_case: PayWithWalletUseCase,
        mock_wallet_repo: AsyncMock,
        mock_transaction_repo: AsyncMock,  # Added as argument
        mock_event_publisher: AsyncMock,  # Added as argument
        pay_with_wallet_command: PayWithWalletCommand,
    ):
        """Tests that WalletNotFoundError is raised if wallet does not exist."""
        # Arrange
        mock_wallet_repo.get_by_id.side_effect = WalletNotFoundError(
            str(pay_with_wallet_command.wallet_id)
        )

        # Act & Assert
        with pytest.raises(WalletNotFoundError) as exc_info:
            await use_case.execute(pay_with_wallet_command)

        mock_wallet_repo.get_by_id.assert_called_once_with(
            pay_with_wallet_command.wallet_id, raise_exception=True
        )
        # Ensure no further calls if wallet not found
        mock_transaction_repo.create.assert_not_called()
        mock_event_publisher.publish_event.assert_not_called()
        assert str(pay_with_wallet_command.wallet_id) in str(exc_info.value)
