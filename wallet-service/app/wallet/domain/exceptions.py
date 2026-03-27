from __future__ import annotations

from typing import Any

from app.shared.base_exceptions import ConflictException, NotFoundException

from app.shared.kernel.exceptions import DomainException


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


class UserNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("User", entity_id)


class UserWalletConflict(ConflictException):
    def __init__(self, reason: str) -> None:
        super().__init__(
            f"User wallet conflict: {reason}",
            details={"reason": reason},
        )
        self.error_code = "USER_WALLET_CONFLICT"
