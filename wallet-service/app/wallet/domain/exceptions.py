from __future__ import annotations

from typing import Any, TYPE_CHECKING

from app.shared.base_exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)
from app.shared.core.exceptions import DomainException

if TYPE_CHECKING:
    from app.wallet.domain.value_objects import WalletId, UserId


class WalletError(DomainException):
    """Base exception for wallet-related errors."""

    pass


class InsufficientFundsError(WalletError):
    """Raised when a wallet has insufficient funds for a transaction."""

    def __init__(self, message: str = "Insufficient funds in wallet.") -> None:
        super().__init__(
            message,
            error_code="INSUFFICIENT_FUNDS",
            status_code=400,
        )


class InvalidTransactionAmountError(WalletError):
    """Raised when a transaction amount is invalid."""

    def __init__(self, message: str = "Invalid transaction amount.") -> None:
        super().__init__(
            message,
            error_code="INVALID_TRANSACTION_AMOUNT",
            status_code=400,
        )


class UnsupportedCurrencyError(WalletError):
    """Raised for unsupported currency."""

    def __init__(self, message: str = "Unsupported currency.") -> None:
        super().__init__(
            message,
            error_code="UNSUPPORTED_CURRENCY",
            status_code=400,
        )


class WalletNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("Wallet", entity_id)

    def __init__(self, wallet_id: WalletId):
        super().__init__("Wallet", wallet_id.value, "wallet_id")

    def __init__(self, user_id: UserId):
        super().__init__("Wallet", user_id.value, "user_id")


class UserNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("User", entity_id)

    def __init__(self, user_id: UserId):
        super().__init__("User", user_id.value, "user_id")


class UserWalletConflict(ConflictException):
    def __init__(self, reason: str) -> None:
        super().__init__(
            f"User wallet conflict: {reason}",
            details={"reason": reason},
        )
        self.error_code = "USER_WALLET_CONFLICT"


class PaymentFailedError(ValidationException):
    """Raised when a payment fails."""

    def __init__(self, message: str = "Payment failed.") -> None:
        super().__init__(message)
        self.error_code = "PAYMENT_FAILED"
        self.status_code = 400
