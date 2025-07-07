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

