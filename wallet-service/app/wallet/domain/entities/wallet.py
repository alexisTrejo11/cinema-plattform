import uuid
from decimal import Decimal
from typing import List, Optional
from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import Money, WalletId
from app.wallet.domain.enums import Currency, TransactionType
from app.wallet.domain.exceptions import (
    InsufficientFundsError,
    InvalidTransactionAmountError,
    UnsupportedCurrencyError,
)
from .wallet_transaction import (
    PaymentDetails,
    WalletTransaction,
)

MIN_CREDIT_ALLOWED_MXN = Money(Decimal("5.00"), Currency.MXN)
MAX_CREDIT_ALLOWED_MXN = Money(Decimal("2000.00"), Currency.MXN)
MIN_CREDIT_ALLOWED_USD = Money(Decimal("0.25"), Currency.USD)
MAX_CREDIT_ALLOWED_USD = Money(Decimal("200.00"), Currency.USD)


class Wallet:
    def __init__(
        self, id: WalletId, user_id: UserId, balance: Money
    ):  # Balance is now Money
        if not isinstance(id, WalletId):
            raise TypeError("Wallet 'id' must be a WalletId object.")
        if not isinstance(user_id, UserId):
            raise TypeError("Wallet 'user_id' must be a UserId object.")
        if not isinstance(balance, Money):
            raise TypeError("Wallet 'balance' must be a Money object.")

        self.id = id
        self.user_id = user_id
        self.balance = balance
        self.transactions: List[WalletTransaction] = []

    def add_credit(
        self,
        payment_details: PaymentDetails,
        amount: Money,
        transaction_type: TransactionType,  # Use TransactionType enum
    ):
        if not isinstance(amount, Money):
            raise TypeError("Amount must be a Money object.")
        if not isinstance(transaction_type, TransactionType):
            raise TypeError("Transaction type must be a TransactionType enum.")
        if amount.amount <= Decimal("0"):
            raise InvalidTransactionAmountError("Credit amount must be positive.")

        self._validate_credit_increase(amount)
        self.balance = self.balance + amount  # Use Money's __add__
        return self.add_transaction(amount, transaction_type, payment_details)

    def remove_credit(
        self,
        payment_details: PaymentDetails,
        amount: Money,
        transaction_type: TransactionType = TransactionType.BUY_PRODUCT,  # Default for payments
    ):
        if not isinstance(amount, Money):
            raise TypeError("Amount must be a Money object.")
        if not isinstance(transaction_type, TransactionType):
            raise TypeError("Transaction type must be a TransactionType enum.")
        if amount.amount <= Decimal("0"):
            raise InvalidTransactionAmountError("Debit amount must be positive.")

        self._validate_credit_decrease(amount)
        self.balance = self.balance - amount  # Use Money's __sub__
        return self.add_transaction(amount, transaction_type, payment_details)

    @staticmethod
    def create(user_id: UserId, initial_currency: Currency = Currency.USD) -> "Wallet":
        # When creating, set an initial balance of 0 for the specified currency
        initial_balance = Money(Decimal("0.00"), initial_currency)
        return Wallet(WalletId(uuid.uuid4()), user_id, initial_balance)

    def add_transaction(
        self,
        amount: Money,
        transaction_type: TransactionType,  # Use TransactionType enum
        payment_details: Optional[PaymentDetails] = None,
    ) -> WalletTransaction:
        if not isinstance(amount, Money):
            raise TypeError("Transaction amount must be a Money object.")
        if not isinstance(transaction_type, TransactionType):
            raise TypeError("Transaction type must be a TransactionType enum.")

        transaction = WalletTransaction(
            transaction_id=uuid.uuid4(),
            wallet_id=self.id,  # WalletId object
            amount=amount,
            payment_details=payment_details,
            transaction_type=transaction_type,
        )
        self.transactions.append(transaction)
        return transaction

    def _validate_credit_increase(self, amount: Money):
        if self.balance.currency != amount.currency:
            raise UnsupportedCurrencyError(
                "Cannot add credit with a different currency than wallet balance."
            )

        if amount.currency == Currency.MXN:
            if not (MIN_CREDIT_ALLOWED_MXN <= amount <= MAX_CREDIT_ALLOWED_MXN):
                raise InvalidTransactionAmountError(
                    f"Invalid Amount for MXN. Range allowed between {MIN_CREDIT_ALLOWED_MXN.amount} to {MAX_CREDIT_ALLOWED_MXN.amount}"
                )
        elif amount.currency == Currency.USD:
            if not (MIN_CREDIT_ALLOWED_USD <= amount <= MAX_CREDIT_ALLOWED_USD):
                raise InvalidTransactionAmountError(
                    f"Invalid Amount for USD. Range allowed between {MIN_CREDIT_ALLOWED_USD.amount} to {MAX_CREDIT_ALLOWED_USD.amount}"
                )
        else:
            raise UnsupportedCurrencyError(
                f"Credit limit validation not defined for currency: {amount.currency.value}"
            )

    def _validate_credit_decrease(self, amount: Money):
        if self.balance.currency != amount.currency:
            raise UnsupportedCurrencyError(
                "Cannot remove credit with a different currency than wallet balance."
            )

        if amount.amount <= Decimal("0"):
            raise InvalidTransactionAmountError("Debit amount must be positive.")

        if self.balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds. Current balance: {self.balance.amount} {self.balance.currency.value}, "
                f"Attempted debit: {amount.amount} {amount.currency.value}"
            )
