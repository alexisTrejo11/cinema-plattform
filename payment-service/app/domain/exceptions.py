"""
Domain Exceptions

Defines custom exceptions for business rule violations and domain-specific errors.
These exceptions represent violations of business invariants and rules.
"""

from typing import Optional


class DomainException(Exception):
    """Base exception for all domain-related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class PaymentException(DomainException):
    """Base exception for payment-related domain errors."""
    pass


class InvalidPaymentAmountException(PaymentException):
    """Raised when payment amount violates business rules."""
    
    def __init__(self, amount: float, minimum: float = 0.01):
        super().__init__(
            f"Invalid payment amount: {amount}. Amount must be greater than {minimum}",
            "INVALID_PAYMENT_AMOUNT"
        )


class PaymentAlreadyProcessedException(PaymentException):
    """Raised when attempting to process an already processed payment."""
    
    def __init__(self, payment_id: str, current_status: str):
        super().__init__(
            f"Payment {payment_id} is already {current_status} and cannot be processed again",
            "PAYMENT_ALREADY_PROCESSED"
        )


class PaymentNotRefundableException(PaymentException):
    """Raised when attempting to refund a non-refundable payment."""
    
    def __init__(self, payment_id: str, reason: str):
        super().__init__(
            f"Payment {payment_id} cannot be refunded: {reason}",
            "PAYMENT_NOT_REFUNDABLE"
        )


class InsufficientFundsException(PaymentException):
    """Raised when wallet has insufficient funds for the transaction."""
    
    def __init__(self, available: float, required: float):
        super().__init__(
            f"Insufficient funds. Available: {available}, Required: {required}",
            "INSUFFICIENT_FUNDS"
        )


class WalletException(DomainException):
    """Base exception for wallet-related domain errors."""
    pass


class InvalidWalletOperationException(WalletException):
    """Raised when attempting an invalid wallet operation."""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"Invalid wallet operation '{operation}': {reason}",
            "INVALID_WALLET_OPERATION"
        )


class WalletNotActiveException(WalletException):
    """Raised when attempting operations on an inactive wallet."""
    
    def __init__(self, wallet_id: str):
        super().__init__(
            f"Wallet {wallet_id} is not active",
            "WALLET_NOT_ACTIVE"
        )


class TransactionException(DomainException):
    """Base exception for transaction-related domain errors."""
    pass


class InvalidTransactionStateException(TransactionException):
    """Raised when transaction state transition is invalid."""
    
    def __init__(self, from_state: str, to_state: str):
        super().__init__(
            f"Invalid state transition from {from_state} to {to_state}",
            "INVALID_TRANSACTION_STATE"
        )
