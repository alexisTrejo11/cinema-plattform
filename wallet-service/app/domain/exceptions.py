class WalletException(Exception):
    """Base exception for wallet-related errors."""

    pass


class InsufficientFundsError(WalletException):
    """Raised when a wallet has insufficient funds for a debit operation."""

    pass


class InvalidTransactionAmountError(WalletException):
    """Raised when a transaction amount is invalid (e.g., negative or zero)."""

    pass


class UserNotFoundException(Exception):
    pass
