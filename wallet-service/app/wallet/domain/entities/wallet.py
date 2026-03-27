import logging
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from ..enums import Currency, TransactionType
from ..value_objects import Charge, Money, WalletId, UserId
from .wallet_transaction import WalletTransaction
from ..validators import WalletDomainValidator

logger = logging.getLogger(__name__)


class Wallet(BaseModel):
    """
    Wallet aggregate root. NOT frozen — balance and transactions mutate over its lifetime.
    Pydantic handles field-type invariants; WalletDomainValidator enforces business rules.
    to_dict() removed — use model_dump() or the dedicated response DTOs.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: WalletId
    user_id: UserId
    balance: Money
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    transactions: List[WalletTransaction] = Field(default_factory=list)

    # ── Factory ─────────────────────────────────────────────────────────────

    @staticmethod
    def create(user_id: UserId, initial_currency: Currency = Currency.USD) -> "Wallet":
        return Wallet(
            id=WalletId(value=uuid.uuid4()),
            user_id=user_id,
            balance=Money(amount=Decimal("0.00"), currency=initial_currency),
        )

    # ── High-level operations ────────────────────────────────────────────────

    def buy_product(self, payment_details, amount: Charge) -> WalletTransaction:
        self.remove_credit(amount)
        # Transaction stores the absolute amount; BUY_PRODUCT type signals debit direction.
        # Previously a negative Charge was created here, which was both misleading and broken.
        transaction_amount = Money(amount=amount.amount, currency=amount.currency)
        return self._create_transaction(
            transaction_amount, TransactionType.BUY_PRODUCT, payment_details
        )

    def buy_credit(self, payment_details, amount: Money) -> WalletTransaction:
        self.add_credit(amount)
        return self._create_transaction(
            amount, TransactionType.ADD_CREDIT, payment_details
        )

    # ── Balance mutation ────────────────────────────────────────────────────

    def add_credit(self, amount: Money) -> None:
        WalletDomainValidator(self).validate_credit_increase(amount)
        self.balance = self.balance + amount

    def remove_credit(self, amount: Charge) -> None:
        WalletDomainValidator(self).validate_credit_decrease(amount)
        self.balance = self.balance - Money(
            amount=amount.amount, currency=amount.currency
        )

    # ── Transaction helpers ─────────────────────────────────────────────────

    def _add_transaction(self, transaction: WalletTransaction) -> WalletTransaction:
        self.transactions.append(transaction)
        self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return transaction

    def _create_transaction(
        self,
        amount: Money,
        transaction_type: TransactionType,
        payment_details,
    ) -> WalletTransaction:
        new_transaction = WalletTransaction.create(
            self.id, amount, transaction_type, payment_details
        )
        self._add_transaction(new_transaction)
        self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        logger.info(
            "Wallet %s recorded %s amount=%s %s",
            self.id.value,
            transaction_type.value,
            amount.amount,
            amount.currency.value,
        )
        return new_transaction

    def set_transactions(self, transactions: List[WalletTransaction]) -> None:
        """Bulk-replace transactions, e.g. after loading from the repository."""
        self.transactions = transactions
        self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    # ── Identity ─────────────────────────────────────────────────────────────
    # Wallets are equal if they share the same id, regardless of other fields.
    # Pydantic's default __eq__ would compare all fields, so we override.

    def display_balance(self) -> str:
        return str(self.balance.amount) + " " + self.balance.currency.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Wallet):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"Wallet(id={self.id.to_string()}, "
            f"user_id={self.user_id.to_string()}, "
            f"balance={self.balance})"
        )
