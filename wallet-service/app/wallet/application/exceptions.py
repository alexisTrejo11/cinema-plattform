"""Application-layer re-exports of wallet domain errors (import stability for infra/tests)."""

from app.wallet.domain.exceptions import (
    InsufficientFundsError,
    InvalidTransactionAmountError,
    UnsupportedCurrencyError,
    UserNotFoundError,
    UserWalletConflict,
    WalletError,
    WalletNotFoundError,
)

__all__ = [
    "WalletError",
    "WalletNotFoundError",
    "UserNotFoundError",
    "UserWalletConflict",
    "InsufficientFundsError",
    "InvalidTransactionAmountError",
    "UnsupportedCurrencyError",
]
