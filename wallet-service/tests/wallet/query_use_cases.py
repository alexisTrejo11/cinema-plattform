import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import WalletId, Money
from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.enums import Currency, TransactionType


from app.wallet.application.use_cases.wallet.wallet_query_usecases import (
    GetWalletByIdUseCase,
    GetWalletsByUserIdUseCase,
)

from app.wallet.presentation.dtos.response import (
    WalletResponse,
    WalletTransactionResponse,
)
from app.wallet.application.query.queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
    QueryBase,
)

from app.wallet.application.exceptions import WalletNotFoundError


# --- Fixtures for Mocks and Dummy Data ---
@pytest.fixture
def mock_wallet_repo():
    """Mocks WalletRepository."""
    return AsyncMock()


@pytest.fixture
def mock_transaction_repo():
    """Mocks WalletTransactionRepository."""
    return AsyncMock()


@pytest.fixture
def dummy_wallet_id() -> WalletId:
    return WalletId(uuid.uuid4())


@pytest.fixture
def dummy_user_id() -> UserId:
    return UserId(uuid.uuid4())


@pytest.fixture
def dummy_wallet_domain(dummy_wallet_id: WalletId, dummy_user_id: UserId) -> Wallet:
    """Provides a dummy Wallet domain object."""
    return Wallet(
        id=dummy_wallet_id,
        user_id=dummy_user_id,
        balance=Money(Decimal("100.00"), Currency.USD),
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        transactions=[],
    )


@pytest.fixture
def dummy_transaction_domain(dummy_wallet_id: WalletId) -> WalletTransaction:
    """Provides a dummy WalletTransaction domain object."""
    return WalletTransaction(
        transaction_id=uuid.uuid4(),
        wallet_id=dummy_wallet_id,
        amount=Money(Decimal("10.00"), Currency.USD),
        transaction_type=TransactionType.ADD_CREDIT,
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
        payment_details=MagicMock(),
    )


@pytest.fixture
def mock_wallet_response_from_domain():
    """Mocks WalletResponse.from_domain static method."""
    # Use patch as it's a static method on a class
    with patch(
        "app.wallet.presentation.dtos.response.WalletResponse.from_domain"
    ) as mock:
        mock_response = MagicMock(spec=WalletResponse)
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def mock_transaction_response_from_domain():
    """Mocks WalletTransactionResponse.from_domain static method."""
    with patch(
        "app.wallet.presentation.dtos.response.WalletTransactionResponse.from_domain"
    ) as mock:
        mock_response = MagicMock(spec=WalletTransactionResponse)
        mock.return_value = mock_response
        yield mock


# --- Tests for GetWalletByIdUseCase ---
class TestGetWalletByIdUseCase:

    @pytest.fixture
    def use_case(self, mock_wallet_repo, mock_transaction_repo):
        return GetWalletByIdUseCase(mock_wallet_repo, mock_transaction_repo)

    @pytest.mark.asyncio
    async def test_execute_success_no_transactions(
        self,
        use_case: GetWalletByIdUseCase,
        mock_wallet_repo: AsyncMock,  # Changed to AsyncMock
        mock_transaction_repo: AsyncMock,  # Changed to AsyncMock
        mock_wallet_response_from_domain: MagicMock,  # Added as argument
        mock_transaction_response_from_domain: MagicMock,  # Added as argument
        dummy_wallet_id: WalletId,
        dummy_wallet_domain: Wallet,
    ):
        """Tests successful retrieval of a wallet by ID without transactions."""
        # Arrange
        query = GetWalletByIdQuery(walletId=dummy_wallet_id, include_transactions=False)
        mock_wallet_repo.get_by_id.return_value = dummy_wallet_domain

        # Act
        response = await use_case.execute(query)

        # Assert
        mock_wallet_repo.get_by_id.assert_called_once_with(
            dummy_wallet_id, raise_exception=True
        )
        mock_wallet_response_from_domain.assert_called_once_with(dummy_wallet_domain)
        mock_transaction_repo.list_by_wallet_id.assert_not_called()  # Should not be called
        mock_transaction_response_from_domain.assert_not_called()  # Should not be called
        assert response == mock_wallet_response_from_domain.return_value
        # Check that transactions attribute is not set or is empty if it exists on the DTO
        assert not hasattr(response, "transactions") or response.transactions == []

    @pytest.mark.asyncio
    async def test_execute_success_with_transactions(
        self,
        use_case: GetWalletByIdUseCase,
        mock_wallet_repo: AsyncMock,  # Changed to AsyncMock
        mock_transaction_repo: AsyncMock,  # Changed to AsyncMock
        mock_wallet_response_from_domain: MagicMock,  # Added as argument
        mock_transaction_response_from_domain: MagicMock,  # Added as argument
        dummy_wallet_id: WalletId,
        dummy_wallet_domain: Wallet,
        dummy_transaction_domain: WalletTransaction,
    ):
        """Tests successful retrieval of a wallet by ID with transactions."""
        # Arrange
        query = GetWalletByIdQuery(
            walletId=dummy_wallet_id,
            include_transactions=True,
            offset=0,
            limit=10,
            sort_by="created_at",
            sort_direction="desc",
        )
        mock_wallet_repo.get_by_id.return_value = dummy_wallet_domain
        mock_transaction_repo.list_by_wallet_id.return_value = [
            dummy_transaction_domain
        ]

        # Act
        response = await use_case.execute(query)

        # Assert
        mock_wallet_repo.get_by_id.assert_called_once_with(
            dummy_wallet_id, raise_exception=True
        )
        mock_wallet_response_from_domain.assert_called_once_with(dummy_wallet_domain)
        mock_transaction_repo.list_by_wallet_id.assert_called_once_with(
            query
        )  # Should pass the query object directly
        mock_transaction_response_from_domain.assert_called_once_with(
            dummy_transaction_domain
        )  # Called once per transaction
        assert len(response.transactions) == 1
        assert (
            response.transactions[0]
            == mock_transaction_response_from_domain.return_value
        )
        assert response == mock_wallet_response_from_domain.return_value

    @pytest.mark.asyncio
    async def test_execute_wallet_not_found(
        self,
        use_case: GetWalletByIdUseCase,
        mock_wallet_repo: AsyncMock,  # Changed to AsyncMock
        mock_wallet_response_from_domain: MagicMock,  # Added as argument
        mock_transaction_repo: AsyncMock,  # Added as argument
        mock_transaction_response_from_domain: MagicMock,  # Added as argument
        dummy_wallet_id: WalletId,
    ):
        """Tests that WalletNotFoundError is re-raised when wallet is not found."""
        # Arrange
        query = GetWalletByIdQuery(walletId=dummy_wallet_id, include_transactions=False)
        mock_wallet_repo.get_by_id.side_effect = WalletNotFoundError(
            str(dummy_wallet_id)
        )

        # Act & Assert
        with pytest.raises(WalletNotFoundError) as exc_info:
            await use_case.execute(query)

        mock_wallet_repo.get_by_id.assert_called_once_with(
            dummy_wallet_id, raise_exception=True
        )
        assert str(dummy_wallet_id) in str(exc_info.value)
        # Ensure DTO creation and transaction fetching are not attempted
        mock_wallet_response_from_domain.assert_not_called()
        mock_transaction_repo.list_by_wallet_id.assert_not_called()
        mock_transaction_response_from_domain.assert_not_called()


# --- Tests for GetWalletsByUserIdUseCase ---
class TestGetWalletsByUserIdUseCase:

    @pytest.fixture
    def use_case(self, mock_wallet_repo, mock_transaction_repo):
        return GetWalletsByUserIdUseCase(mock_wallet_repo, mock_transaction_repo)

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        use_case: GetWalletsByUserIdUseCase,
        mock_wallet_repo: MagicMock,
        mock_transaction_repo: MagicMock,
        mock_wallet_response_from_domain: MagicMock,
        dummy_user_id: UserId,
        dummy_wallet_domain: Wallet,
    ):
        """Tests successful retrieval of a wallet by user ID."""
        # Arrange
        query = GetWalletByUserIdQuery(
            userId=dummy_user_id,
            include_transactions=False,  # The current use case implementation does NOT use this
            offset=0,
            limit=10,
            sort_by="created_at",
            sort_direction="asc",
        )
        mock_wallet_repo.get_by_user_id.return_value = dummy_wallet_domain

        # Act
        response = await use_case.execute(query)

        # Assert
        mock_wallet_repo.get_by_user_id.assert_called_once_with(
            user_id=dummy_user_id, raise_exception=True
        )
        mock_wallet_response_from_domain.assert_called_once_with(dummy_wallet_domain)
        # IMPORTANT: Based on your provided GetWalletsByUserIdUseCase,
        # the _get_transactions method is *never called* by execute.
        # So, we assert it's not called.
        mock_transaction_repo.list_by_wallet_id.assert_not_called()
        assert response == mock_wallet_response_from_domain.return_value

    @pytest.mark.asyncio
    async def test_execute_wallet_not_found(
        self,
        use_case: GetWalletsByUserIdUseCase,
        mock_wallet_repo: AsyncMock,
        mock_wallet_response_from_domain: MagicMock,
        mock_transaction_repo: AsyncMock,
        mock_transaction_response_from_domain: MagicMock,
        dummy_user_id: UserId,
    ):
        """Tests that WalletNotFoundError is re-raised when wallet for user is not found."""
        # Arrange
        query = GetWalletByUserIdQuery(userId=dummy_user_id, include_transactions=False)
        mock_wallet_repo.get_by_user_id.side_effect = WalletNotFoundError(
            str(dummy_user_id)
        )

        # Act & Assert
        with pytest.raises(WalletNotFoundError) as exc_info:
            await use_case.execute(query)

        mock_wallet_repo.get_by_user_id.assert_called_once_with(
            user_id=dummy_user_id, raise_exception=True
        )
        assert str(dummy_user_id) in str(exc_info.value)

        mock_wallet_response_from_domain.assert_not_called()
        mock_transaction_repo.list_by_wallet_id.assert_not_called()
        mock_transaction_response_from_domain.assert_not_called()
