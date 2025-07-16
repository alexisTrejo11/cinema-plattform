from .exceptions import *
from .value_objects import Money, Decimal, Currency, WalletId, Charge
from app.user.domain.value_objects import UserId

MIN_CREDIT_ALLOWED_MXN = Money(Decimal("5.00"), Currency.MXN)
MAX_CREDIT_ALLOWED_MXN = Money(Decimal("2000.00"), Currency.MXN)
MIN_CREDIT_ALLOWED_USD = Money(Decimal("0.25"), Currency.USD)
MAX_CREDIT_ALLOWED_USD = Money(Decimal("200.00"), Currency.USD)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..domain.entities.wallet import Wallet


class WalletDomainValidator:
    def __init__(self, wallet: 'Wallet') -> None:
        self.wallet = wallet
        self.validate_data_types()
        
    def validate_data_types(self):
        if not isinstance(self.wallet.id, WalletId):
            raise TypeError("Wallet 'id' must be a WalletId object.")
        if not isinstance(self.wallet.user_id, UserId):
            raise TypeError("Wallet 'user_id' must be a UserId object.")
        if not isinstance(self.wallet.balance, Money):
            raise TypeError("Wallet 'balance' must be a Money object.")


    def validate_credit_increase(self, amount: Money):
        if self.wallet.balance.currency != amount.currency:
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

    def validate_credit_decrease(self, amount: Charge):
        if self.wallet.balance.currency != amount.currency:
            raise UnsupportedCurrencyError(
                "Cannot remove credit with a different currency than wallet balance."
            )

        if amount.amount > Decimal("0"):
            raise InvalidTransactionAmountError("Charge amount must be negative or zero.")

        if self.wallet.balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds. Current balance: {self.wallet.balance.amount} {self.wallet.balance.currency.value}, "
                f"Attempted debit: {amount.amount} {amount.currency.value}"
            )