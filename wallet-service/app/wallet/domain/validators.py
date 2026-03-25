from decimal import Decimal
from typing import TYPE_CHECKING

from .exceptions import (
    InsufficientFundsError,
    InvalidTransactionAmountError,
    UnsupportedCurrencyError,
)
from .value_objects import Charge, Currency, Money

if TYPE_CHECKING:
    from .entities.wallet import Wallet


# ── Per-currency credit limits ───────────────────────────────────────────────

MIN_CREDIT_ALLOWED_MXN = Money(amount=Decimal("5.00"), currency=Currency.MXN)
MAX_CREDIT_ALLOWED_MXN = Money(amount=Decimal("2000.00"), currency=Currency.MXN)
MIN_CREDIT_ALLOWED_USD = Money(amount=Decimal("0.25"), currency=Currency.USD)
MAX_CREDIT_ALLOWED_USD = Money(amount=Decimal("200.00"), currency=Currency.USD)


class WalletDomainValidator:
    """
    Enforces wallet business rules.
    Field-type invariants (id is WalletId, balance is Money, etc.) are now
    handled by Pydantic on construction, so validate_data_types() is removed.
    """

    def __init__(self, wallet: "Wallet") -> None:
        self.wallet = wallet

    def validate_credit_increase(self, amount: Money) -> None:
        if self.wallet.balance.currency != amount.currency:
            raise UnsupportedCurrencyError(
                "Cannot add credit with a different currency than wallet balance."
            )

        if amount.currency == Currency.MXN:
            if not (MIN_CREDIT_ALLOWED_MXN <= amount <= MAX_CREDIT_ALLOWED_MXN):
                raise InvalidTransactionAmountError(
                    f"Invalid Amount for MXN. Range allowed between "
                    f"{MIN_CREDIT_ALLOWED_MXN.amount} to {MAX_CREDIT_ALLOWED_MXN.amount}"
                )
        elif amount.currency == Currency.USD:
            if not (MIN_CREDIT_ALLOWED_USD <= amount <= MAX_CREDIT_ALLOWED_USD):
                raise InvalidTransactionAmountError(
                    f"Invalid Amount for USD. Range allowed between "
                    f"{MIN_CREDIT_ALLOWED_USD.amount} to {MAX_CREDIT_ALLOWED_USD.amount}"
                )
        else:
            raise UnsupportedCurrencyError(
                f"Credit limit validation not defined for currency: {amount.currency.value}"
            )

    def validate_credit_decrease(self, amount: Charge) -> None:
        if self.wallet.balance.currency != amount.currency:
            raise UnsupportedCurrencyError(
                "Cannot remove credit with a different currency than wallet balance."
            )

        # Charge must be positive — it represents the magnitude of the deduction.
        # Previously the check was inverted (rejected positive values), which made
        # every real payment fail. Fixed here.
        if amount.amount <= Decimal("0"):
            raise InvalidTransactionAmountError("Charge amount must be positive.")

        # Compare against wallet balance using a Money instance for proper currency check.
        charge_as_money = Money(amount=amount.amount, currency=amount.currency)
        if self.wallet.balance < charge_as_money:
            raise InsufficientFundsError(
                f"Insufficient funds. Current balance: "
                f"{self.wallet.balance.amount} {self.wallet.balance.currency.value}, "
                f"Attempted debit: {amount.amount} {amount.currency.value}"
            )
