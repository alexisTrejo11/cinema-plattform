import pytest
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from unittest.mock import MagicMock, patch

from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import Money, WalletId, Charge
from app.wallet.domain.enums import Currency, TransactionType
from app.wallet.domain.entities.wallet_transaction import (
    PaymentDetails,
    WalletTransaction,
)
from app.wallet.domain.entities.wallet import Wallet

from app.wallet.domain.validators import WalletDomainValidator as WalletValidator


# --- Fixtures for common test data ---
@pytest.fixture
def sample_user_id() -> UserId:
    return UserId(uuid.uuid4())


@pytest.fixture
def sample_wallet_id() -> WalletId:
    return WalletId(uuid.uuid4())


@pytest.fixture
def initial_balance() -> Money:
    return Money(Decimal("100.00"), Currency.USD)


@pytest.fixture
def mock_wallet_validator():
    """Mocks the WalletDomainValidator to control its behavior."""
    validator = MagicMock()
    # By default, mock methods do nothing, but you can configure them
    # validator.validate_credit_increase.return_value = None # No return value needed
    # validator.validate_credit_decrease.return_value = None
    return validator


@pytest.fixture
def mock_wallet_transaction_create():
    """Mocks the static create method of WalletTransaction."""
    with patch(
        "app.wallet.domain.entities.wallet_transaction.WalletTransaction.create"
    ) as mock_create:
        mock_transaction = MagicMock(spec=WalletTransaction)
        mock_transaction.to_dict.return_value = {
            "id": str(uuid.uuid4()),
            "amount": "10.00",
        }  # For to_dict test
        mock_create.return_value = mock_transaction
        yield mock_create


@pytest.fixture
def sample_payment_details() -> PaymentDetails:
    """A simple mock or dummy for PaymentDetails."""
    return MagicMock(spec=PaymentDetails)


@pytest.fixture
def default_wallet(
    sample_wallet_id: WalletId,
    sample_user_id: UserId,
    initial_balance: Money,
    mock_wallet_validator: MagicMock,
) -> Wallet:
    """Provides a basic Wallet instance for testing."""
    wallet = Wallet(
        id=sample_wallet_id,
        user_id=sample_user_id,
        balance=initial_balance,
    )
    # Replace the actual validator with the mock for the test instance
    wallet._validator = mock_wallet_validator
    return wallet


# --- Test Cases for Wallet Domain Class ---
class TestWalletDomain:

    def test_wallet_initialization_and_properties(
        self,
        sample_wallet_id: WalletId,
        sample_user_id: UserId,
        initial_balance: Money,
        mock_wallet_validator: MagicMock,
    ):
        """Tests that Wallet initializes correctly and properties work."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        wallet = Wallet(
            id=sample_wallet_id,
            user_id=sample_user_id,
            balance=initial_balance,
        )
        wallet._validator = mock_wallet_validator  # Inject mock

        assert wallet.id == sample_wallet_id
        assert wallet.user_id == sample_user_id
        assert wallet.balance == initial_balance
        assert wallet.transactions == []  # Should be empty initially
        assert isinstance(wallet.created_at, datetime)
        assert isinstance(wallet.updated_at, datetime)
        # Check if timestamps are close to now (within a few seconds)
        assert (
            datetime.now(timezone.utc).replace(tzinfo=None) - wallet.created_at
        ).total_seconds() < 2
        assert (
            datetime.now(timezone.utc).replace(tzinfo=None) - wallet.updated_at
        ).total_seconds() < 2

        # Test with provided timestamps and transactions
        past_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).replace(
            tzinfo=None
        )
        mock_transaction_list = [
            MagicMock(spec=WalletTransaction),
            MagicMock(spec=WalletTransaction),
        ]
        wallet_with_history = Wallet(
            id=WalletId(uuid.uuid4()),
            user_id=UserId(uuid.uuid4()),
            balance=Money(Decimal("200.00"), Currency.EUR),
            created_at=past_time,
            updated_at=past_time,
            transactions=mock_transaction_list,
        )
        assert wallet_with_history.created_at == past_time
        assert wallet_with_history.updated_at == past_time
        assert (
            wallet_with_history.transactions == mock_transaction_list
        )  # Verify it uses the provided list (copy)
        assert (
            wallet_with_history.transactions is not mock_transaction_list
        )  # Ensure it's a copy

    def test_wallet_create_static_method(self, sample_user_id: UserId):
        """Tests the create static method."""
        wallet = Wallet.create(sample_user_id)

        assert isinstance(wallet, Wallet)
        assert isinstance(wallet.id, WalletId)
        assert isinstance(wallet.user_id, UserId)
        assert wallet.user_id == sample_user_id
        assert wallet.balance == Money(Decimal("0.00"), Currency.USD)
        assert wallet.transactions == []
        assert isinstance(wallet.created_at, datetime)
        assert isinstance(wallet.updated_at, datetime)

        # Test with specific currency
        wallet_eur = Wallet.create(sample_user_id, initial_currency=Currency.EUR)
        assert wallet_eur.balance.currency == Currency.EUR

    def test_add_credit(self, default_wallet: Wallet, mock_wallet_validator: MagicMock):
        """Tests adding credit to the wallet."""
        amount_to_add = Money(Decimal("50.00"), Currency.USD)
        initial_balance = (
            default_wallet.balance
        )  # Use the Money object, not just amount

        default_wallet.add_credit(amount_to_add)

        assert (
            default_wallet.balance.amount
            == initial_balance.amount + amount_to_add.amount
        )
        assert default_wallet.balance.currency == initial_balance.currency
        mock_wallet_validator.validate_credit_increase.assert_called_once_with(
            amount_to_add
        )

    def test_remove_credit(
        self, default_wallet: Wallet, mock_wallet_validator: MagicMock
    ):
        """Tests removing credit from the wallet."""
        amount_to_remove = Charge(Decimal("30.00"), Currency.USD)
        initial_balance = (
            default_wallet.balance
        )  # Use the Money object, not just amount

        default_wallet.remove_credit(amount_to_remove)

        assert (
            default_wallet.balance.amount
            == initial_balance.amount - amount_to_remove.amount
        )
        assert default_wallet.balance.currency == initial_balance.currency
        mock_wallet_validator.validate_credit_decrease.assert_called_once_with(
            amount_to_remove
        )

    def test_buy_credit(
        self,
        default_wallet: Wallet,
        sample_payment_details: PaymentDetails,
        mock_wallet_validator: MagicMock,
        mock_wallet_transaction_create: MagicMock,
    ):
        """Tests the buy_credit method."""
        amount_to_buy = Money(Decimal("75.00"), Currency.USD)
        initial_balance = default_wallet.balance.amount
        initial_updated_at = default_wallet.updated_at

        transaction = default_wallet.buy_credit(sample_payment_details, amount_to_buy)

        # Assert add_credit was called and balance updated
        assert default_wallet.balance.amount == initial_balance + amount_to_buy.amount
        mock_wallet_validator.validate_credit_increase.assert_called_once_with(
            amount_to_buy
        )

        # Assert _create_transaction was called correctly
        mock_wallet_transaction_create.assert_called_once_with(
            default_wallet.id,
            amount_to_buy,
            TransactionType.ADD_CREDIT,
            sample_payment_details,
        )
        # Assert transaction was added to the list
        assert len(default_wallet.transactions) == 1
        assert default_wallet.transactions[0] == transaction
        # Assert updated_at was updated
        assert default_wallet.updated_at > initial_updated_at
        assert transaction == mock_wallet_transaction_create.return_value

    def test_buy_product(
        self,
        default_wallet: Wallet,
        sample_payment_details: PaymentDetails,
        mock_wallet_validator: MagicMock,
        mock_wallet_transaction_create: MagicMock,
    ):
        """Tests the buy_product method."""
        amount_to_buy = Charge(Decimal("25.00"), Currency.USD)
        initial_balance = default_wallet.balance.amount
        initial_updated_at = default_wallet.updated_at

        transaction = default_wallet.buy_product(sample_payment_details, amount_to_buy)

        # Assert remove_credit was called and balance updated
        assert default_wallet.balance.amount == initial_balance - amount_to_buy.amount
        mock_wallet_validator.validate_credit_decrease.assert_called_once_with(
            amount_to_buy
        )

        # Assert _create_transaction was called correctly (note: transaction_amount is negative for debit)
        expected_transaction_amount = Charge(Decimal("-25.00"), Currency.USD)
        mock_wallet_transaction_create.assert_called_once_with(
            default_wallet.id,
            expected_transaction_amount,
            TransactionType.BUY_PRODUCT,
            sample_payment_details,
        )
        # Assert transaction was added to the list
        assert len(default_wallet.transactions) == 1
        assert default_wallet.transactions[0] == transaction
        # Assert updated_at was updated
        assert default_wallet.updated_at > initial_updated_at
        assert transaction == mock_wallet_transaction_create.return_value

    def test_set_transactions(self, default_wallet: Wallet):
        """Tests setting the transactions list."""
        initial_updated_at = default_wallet.updated_at
        mock_transactions_list = [
            MagicMock(spec=WalletTransaction),
            MagicMock(spec=WalletTransaction),
        ]

        default_wallet.set_transactions(mock_transactions_list)

        assert default_wallet.transactions == mock_transactions_list
        assert (
            default_wallet.transactions is not mock_transactions_list
        )  # Should be a copy
        assert (
            default_wallet.updated_at > initial_updated_at
        )  # Updated timestamp should be newer

        # Test setting an empty list
        default_wallet.set_transactions([])
        assert default_wallet.transactions == []

    def test_to_dict_method(
        self, default_wallet: Wallet, mock_wallet_transaction_create: MagicMock
    ):
        """Tests the to_dict serialization method."""
        # Set up the mock transaction attributes properly
        mock_transaction_id = uuid.uuid4()
        mock_transaction = MagicMock(spec=WalletTransaction)
        mock_transaction.id = MagicMock()
        mock_transaction.id.value = mock_transaction_id
        mock_transaction.wallet_id = MagicMock()
        mock_transaction.wallet_id.value = default_wallet.id.value
        mock_transaction.amount = Money(Decimal("10.00"), Currency.USD)
        mock_transaction.type = TransactionType.ADD_CREDIT
        mock_transaction.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        mock_transaction.to_dict.return_value = {
            "id": str(mock_transaction_id),
            "wallet_id": str(default_wallet.id.value),
            "amount": "10.00",
            "currency": "USD",
            "type": "ADD_CREDIT",
            "created_at": mock_transaction.created_at.isoformat(),
            "payment_details": {},
        }

        mock_wallet_transaction_create.return_value = mock_transaction

        # Add a transaction to the wallet for a more complete test
        transaction = default_wallet.buy_credit(
            MagicMock(), Money(Decimal("10.00"), Currency.USD)
        )

        wallet_dict = default_wallet.to_dict()

        assert isinstance(wallet_dict, dict)
        assert wallet_dict["id"] == default_wallet.id.to_string()
        assert wallet_dict["user_id"] == default_wallet.user_id.to_string()
        assert wallet_dict["balance"] == str(default_wallet.balance.amount)
        assert wallet_dict["currency"] == default_wallet.balance.currency.value
        assert wallet_dict["created_at"] == default_wallet.created_at.isoformat()
        assert wallet_dict["updated_at"] == default_wallet.updated_at.isoformat()
        assert isinstance(wallet_dict["transactions"], list)
        assert len(wallet_dict["transactions"]) == 1
        assert wallet_dict["transactions"][0]["id"] == str(mock_transaction_id)

    def test_wallet_equality(self, sample_user_id: UserId, initial_balance: Money):
        """Tests __eq__ and __hash__ methods."""
        wallet_id = WalletId(uuid.uuid4())
        wallet1 = Wallet(wallet_id, sample_user_id, initial_balance)
        wallet2 = Wallet(
            wallet_id, sample_user_id, initial_balance
        )  # Same ID, different instance
        wallet3 = Wallet(
            WalletId(uuid.uuid4()), sample_user_id, initial_balance
        )  # Different ID

        assert wallet1 == wallet2
        assert wallet1 != wallet3
        assert hash(wallet1) == hash(wallet2)
        assert hash(wallet1) != hash(wallet3)

        # Test equality with non-Wallet object
        assert wallet1 != "not a wallet"
        assert not (wallet1 == None)  # noqa: E711

    def test_wallet_repr(self, default_wallet: Wallet):
        """Tests the __repr__ method."""
        expected_repr = (
            f"Wallet(id={default_wallet.id.to_string()}, "
            f"user_id={default_wallet.user_id.to_string()}, "
            f"balance={default_wallet.balance})"
        )
        assert repr(default_wallet) == expected_repr
