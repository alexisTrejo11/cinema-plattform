from app.shared.base_exceptions import (
    DomainException,
    NotFoundException,
    ValidationException,
)
from typing import Any
from http import HTTPStatus


class WalletError(DomainException):
    """Base exception for wallet-related errors."""

    pass


class InsufficientFundsError(WalletError):
    """Raised when a wallet has insufficient funds for a transaction."""

    def __init__(self, message="Insufficient funds in wallet."):
        self.message = message
        super().__init__(self.message)


class InvalidTransactionAmountError(WalletError):
    """Raised when a transaction amount is invalid (e.g., out of allowed range, negative for credit)."""

    def __init__(self, message="Invalid transaction amount."):
        self.message = message
        super().__init__(self.message)


class WalletNotFoundError(WalletError):
    """Raised when a wallet is not found."""

    def __init__(self, message="Wallet not found."):
        self.message = message
        super().__init__(self.message)


class UnsupportedCurrencyError(WalletError):
    """Raised when an operation is attempted with an unsupported currency."""

    def __init__(self, message="Unsupported currency."):
        self.message = message
        super().__init__(self.message)


class WalletNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("Wallet", entity_id)


class UserNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("User", entity_id)


class UserWalletConflict(ValidationException):
    def __init__(self, reason: str):
        super().__init__("User", reason)

    status_code = HTTPStatus.CONFLICT
