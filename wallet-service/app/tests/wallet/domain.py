"""
Domain tests for Wallet aggregate.

Key changes from the old pure-class version:
- All value-object constructors now use keyword arguments (Pydantic requirement).
- PaymentDetails is imported from value_objects, not wallet_transaction.
- _validator injection replaced: Wallet no longer stores a _validator attribute;
  WalletDomainValidator is instantiated inline. Tests that need to bypass
  business-rule validation now patch the class directly.
- Wallet.transactions is a direct field reference — set_transactions does NOT copy.
- to_dict() removed; model_dump() used instead.
- buy_product now stores Money(abs_amount) in the transaction (not Charge(-amount)).
"""

import pytest
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from unittest.mock import MagicMock, patch

from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import Charge, Money, PaymentDetails, WalletId
from app.wallet.domain.enums import Currency, TransactionType
from app.wallet.domain.entities.wallet_transaction import WalletTransaction
from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.validators import WalletDomainValidator as WalletValidator


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_user_id() -> UserId:
    return UserId(uuid.uuid4())


@pytest.fixture
def sample_wallet_id() -> WalletId:
    # Pydantic models require keyword arguments
    return WalletId(value=uuid.uuid4())


@pytest.fixture
def initial_balance() -> Money:
    return Money(amount=Decimal("100.00"), currency=Currency.USD)


@pytest.fixture
def sample_payment_details() -> PaymentDetails:
    return MagicMock(spec=PaymentDetails)


@pytest.fixture
def mock_wallet_transaction_create():
    """Mocks WalletTransaction.create to return a controlled mock."""
    with patch(
        "app.wallet.domain.entities.wallet_transaction.WalletTransaction.create"
    ) as mock_create:
        mock_transaction = MagicMock(spec=WalletTransaction)
        mock_create.return_value = mock_transaction
        yield mock_create


@pytest.fixture
def default_wallet(
    sample_wallet_id: WalletId,
    sample_user_id: UserId,
    initial_balance: Money,
) -> Wallet:
    """Provides a Wallet with a 100 USD balance for testing."""
    return Wallet(
        id=sample_wallet_id,
        user_id=sample_user_id,
        balance=initial_balance,
    )


# ── Tests ────────────────────────────────────────────────────────────────────

class TestWalletDomain:

    def test_wallet_initialization_and_properties(
        self,
        sample_wallet_id: WalletId,
        sample_user_id: UserId,
        initial_balance: Money,
    ):
        """Wallet initialises correctly and all public fields are accessible."""
        wallet = Wallet(
            id=sample_wallet_id,
            user_id=sample_user_id,
            balance=initial_balance,
        )

        assert wallet.id == sample_wallet_id
        assert wallet.user_id == sample_user_id
        assert wallet.balance == initial_balance
        assert wallet.transactions == []
        assert isinstance(wallet.created_at, datetime)
        assert isinstance(wallet.updated_at, datetime)

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        assert (now - wallet.created_at).total_seconds() < 2
        assert (now - wallet.updated_at).total_seconds() < 2

        past_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).replace(tzinfo=None)
        mock_transaction_list = [
            MagicMock(spec=WalletTransaction),
            MagicMock(spec=WalletTransaction),
        ]
        wallet_with_history = Wallet(
            id=WalletId(value=uuid.uuid4()),
            user_id=UserId(uuid.uuid4()),
            balance=Money(amount=Decimal("200.00"), currency=Currency.EUR),
            created_at=past_time,
            updated_at=past_time,
            transactions=mock_transaction_list,
        )
        assert wallet_with_history.created_at == past_time
        assert wallet_with_history.updated_at == past_time
        # Pydantic stores the provided list directly (no defensive copy)
        assert wallet_with_history.transactions == mock_transaction_list

    def test_wallet_create_static_method(self, sample_user_id: UserId):
        """Wallet.create returns a zero-balance wallet with the correct currency."""
        wallet = Wallet.create(sample_user_id)

        assert isinstance(wallet, Wallet)
        assert isinstance(wallet.id, WalletId)
        assert isinstance(wallet.user_id, UserId)
        assert wallet.user_id == sample_user_id
        assert wallet.balance == Money(amount=Decimal("0.00"), currency=Currency.USD)
        assert wallet.transactions == []
        assert isinstance(wallet.created_at, datetime)
        assert isinstance(wallet.updated_at, datetime)

        wallet_eur = Wallet.create(sample_user_id, initial_currency=Currency.EUR)
        assert wallet_eur.balance.currency == Currency.EUR

    def test_add_credit(self, default_wallet: Wallet):
        """add_credit increases balance by the given amount."""
        amount_to_add = Money(amount=Decimal("50.00"), currency=Currency.USD)
        initial_balance = default_wallet.balance

        # Real validator runs — 50 USD is within the allowed range
        default_wallet.add_credit(amount_to_add)

        assert default_wallet.balance.amount == initial_balance.amount + amount_to_add.amount
        assert default_wallet.balance.currency == initial_balance.currency

    def test_remove_credit(self, default_wallet: Wallet):
        """remove_credit decreases balance by the Charge amount."""
        amount_to_remove = Charge(amount=Decimal("30.00"), currency=Currency.USD)
        initial_balance = default_wallet.balance

        default_wallet.remove_credit(amount_to_remove)

        assert default_wallet.balance.amount == initial_balance.amount - amount_to_remove.amount
        assert default_wallet.balance.currency == initial_balance.currency

    def test_buy_credit(
        self,
        default_wallet: Wallet,
        sample_payment_details: PaymentDetails,
        mock_wallet_transaction_create: MagicMock,
    ):
        """buy_credit increases balance and records an ADD_CREDIT transaction."""
        amount_to_buy = Money(amount=Decimal("75.00"), currency=Currency.USD)
        initial_balance = default_wallet.balance.amount
        initial_updated_at = default_wallet.updated_at

        transaction = default_wallet.buy_credit(sample_payment_details, amount_to_buy)

        assert default_wallet.balance.amount == initial_balance + amount_to_buy.amount
        mock_wallet_transaction_create.assert_called_once_with(
            default_wallet.id,
            amount_to_buy,
            TransactionType.ADD_CREDIT,
            sample_payment_details,
        )
        assert len(default_wallet.transactions) == 1
        assert default_wallet.transactions[0] == transaction
        assert default_wallet.updated_at > initial_updated_at
        assert transaction == mock_wallet_transaction_create.return_value

    def test_buy_product(
        self,
        default_wallet: Wallet,
        sample_payment_details: PaymentDetails,
        mock_wallet_transaction_create: MagicMock,
    ):
        """
        buy_product deducts balance and records a BUY_PRODUCT transaction
        with the absolute (positive) amount — direction is indicated by transaction_type.
        Old behaviour stored Charge(-amount); fixed to store Money(amount).
        """
        amount_to_buy = Charge(amount=Decimal("25.00"), currency=Currency.USD)
        initial_balance = default_wallet.balance.amount
        initial_updated_at = default_wallet.updated_at

        transaction = default_wallet.buy_product(sample_payment_details, amount_to_buy)

        assert default_wallet.balance.amount == initial_balance - amount_to_buy.amount

        # Transaction stores the positive magnitude; BUY_PRODUCT type signals debit direction
        expected_transaction_amount = Money(amount=Decimal("25.00"), currency=Currency.USD)
        mock_wallet_transaction_create.assert_called_once_with(
            default_wallet.id,
            expected_transaction_amount,
            TransactionType.BUY_PRODUCT,
            sample_payment_details,
        )
        assert len(default_wallet.transactions) == 1
        assert default_wallet.transactions[0] == transaction
        assert default_wallet.updated_at > initial_updated_at
        assert transaction == mock_wallet_transaction_create.return_value

    def test_set_transactions(self, default_wallet: Wallet):
        """set_transactions replaces the transaction list and bumps updated_at."""
        initial_updated_at = default_wallet.updated_at
        mock_transactions_list = [
            MagicMock(spec=WalletTransaction),
            MagicMock(spec=WalletTransaction),
        ]

        default_wallet.set_transactions(mock_transactions_list)

        assert default_wallet.transactions == mock_transactions_list
        # Pydantic assigns the list reference directly — no copy
        assert default_wallet.transactions is mock_transactions_list
        assert default_wallet.updated_at > initial_updated_at

        default_wallet.set_transactions([])
        assert default_wallet.transactions == []

    def test_model_dump(
        self, default_wallet: Wallet, mock_wallet_transaction_create: MagicMock
    ):
        """
        model_dump() replaces the removed to_dict().
        Verifies that the Pydantic-native serialisation contains the expected keys.
        """
        mock_wallet_transaction_create.return_value = MagicMock(spec=WalletTransaction)

        default_wallet.buy_credit(
            MagicMock(), Money(amount=Decimal("10.00"), currency=Currency.USD)
        )

        wallet_dict = default_wallet.model_dump()

        assert isinstance(wallet_dict, dict)
        # id is a nested WalletId dict; to_string() is still available on the field object
        assert wallet_dict["id"]["value"] == default_wallet.id.value
        assert wallet_dict["user_id"] == default_wallet.user_id.value
        assert wallet_dict["balance"]["amount"] == default_wallet.balance.amount
        assert wallet_dict["balance"]["currency"] == default_wallet.balance.currency
        assert isinstance(wallet_dict["transactions"], list)

    def test_wallet_equality(self, sample_user_id: UserId, initial_balance: Money):
        """Wallets with the same id compare equal regardless of other fields."""
        wallet_id = WalletId(value=uuid.uuid4())
        wallet1 = Wallet(id=wallet_id, user_id=sample_user_id, balance=initial_balance)
        wallet2 = Wallet(id=wallet_id, user_id=sample_user_id, balance=initial_balance)
        wallet3 = Wallet(
            id=WalletId(value=uuid.uuid4()), user_id=sample_user_id, balance=initial_balance
        )

        assert wallet1 == wallet2
        assert wallet1 != wallet3
        assert hash(wallet1) == hash(wallet2)
        assert hash(wallet1) != hash(wallet3)

        assert wallet1 != "not a wallet"
        assert not (wallet1 == None)  # noqa: E711

    def test_wallet_repr(self, default_wallet: Wallet):
        """__repr__ renders id, user_id and balance."""
        expected_repr = (
            f"Wallet(id={default_wallet.id.to_string()}, "
            f"user_id={default_wallet.user_id.to_string()}, "
            f"balance={default_wallet.balance})"
        )
        assert repr(default_wallet) == expected_repr
