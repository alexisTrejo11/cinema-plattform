import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import Money, WalletId, Charge
from app.wallet.domain.enums import Currency, TransactionType
from .wallet_transaction import PaymentDetails, WalletTransaction
from ..validators import WalletDomainValidator as WalletValidator


class Wallet:
    def __init__(
        self,
        id: WalletId,
        user_id: UserId,
        balance: Money,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        transactions: Optional[List[WalletTransaction]] = None,
    ):
        self._id = id
        self._user_id = user_id
        self._balance = balance
        self._created_at = (
            created_at
            if created_at
            else datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self._updated_at = (
            updated_at
            if updated_at
            else datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self._transactions: List[WalletTransaction] = (
            transactions if transactions is not None else []
        )

        self._validator = WalletValidator(self)

    @property
    def id(self) -> WalletId:
        return self._id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def balance(self) -> Money:
        return self._balance

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def transactions(self) -> List[WalletTransaction]:
        return list(self._transactions)

    @staticmethod
    def create(user_id: UserId, initial_currency: Currency = Currency.USD) -> "Wallet":
        initial_balance = Money(Decimal("0.00"), initial_currency)
        wallet_id = WalletId(uuid.uuid4())
        return Wallet(wallet_id, user_id, initial_balance)

    def buy_product(
        self, payment_details: PaymentDetails, amount: Charge
    ) -> WalletTransaction:
        self.remove_credit(amount)  # This already calls validate_credit_decrease

        transaction_amount = Charge(Decimal(-abs(amount.amount)), amount.currency)
        return self._create_transaction(
            transaction_amount, TransactionType.BUY_PRODUCT, payment_details
        )

    def buy_credit(
        self, payment_details: PaymentDetails, amount: Money
    ) -> WalletTransaction:
        self.add_credit(amount)
        return self._create_transaction(
            amount, TransactionType.ADD_CREDIT, payment_details
        )

    def add_credit(self, amount: Money) -> None:
        self._validator.validate_credit_increase(amount)
        self._balance += amount

    def remove_credit(self, amount: Charge) -> None:
        self._validator.validate_credit_decrease(amount)
        self._balance -= Money(amount.amount, amount.currency)

    def _add_transaction(self, transaction: WalletTransaction) -> WalletTransaction:
        """
        Internal method to add a transaction to the wallet's list.
        """
        # TODO: CHECK
        self._transactions.append(transaction)
        self._updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return transaction

    def _create_transaction(
        self,
        amount: Money,
        transaction_type: TransactionType,
        payment_details: PaymentDetails,
    ) -> WalletTransaction:
        """
        Creates and adds a new WalletTransaction to this wallet.
        """
        new_transaction = WalletTransaction.create(
            self.id, amount, transaction_type, payment_details
        )
        self._add_transaction(new_transaction)
        self._updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return new_transaction

    def set_transactions(self, transactions: List[WalletTransaction]) -> None:
        """
        Allows setting the transactions list from the repository,
        e.g., after fetching a wallet with its transactions.
        """
        # Consider if you want to replace or extend
        self._transactions = transactions
        self._updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def to_dict(self) -> dict:
        """
        Converts the Wallet domain object to a dictionary for DTOs/serialization.
        """
        return {
            "id": self.id.to_string(),
            "user_id": self.user_id.to_string(),
            "balance": str(self.balance.amount),
            "currency": self.balance.currency.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Wallet):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Wallet(id={self.id.to_string()}, user_id={self.user_id.to_string()}, balance={self.balance})"
