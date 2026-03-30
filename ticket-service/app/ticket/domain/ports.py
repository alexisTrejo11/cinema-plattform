"""Outbound ports (interfaces) for cross-service integrations.

Authoritative seat checks and payment capture should go through gRPC (or HTTP)
adapters in infrastructure; local Mongo/Postgres replicas back read-heavy paths.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class PaymentAuthorizationRequest:
    """Values needed to authorize a card/wallet charge before issuing tickets."""

    amount: Decimal
    currency: str
    customer_id: int
    idempotency_key: str
    payment_method: str
    payment_token: str
    customer_ip: Optional[str] = None


@dataclass(frozen=True)
class PaymentAuthorizationResult:
    transaction_id: str
    authorized: bool


@dataclass(frozen=True)
class PaymentRefundRequest:
    ticket_id: int
    transaction_id: str
    amount: Decimal
    currency: str
    reason: Optional[str] = None


@dataclass(frozen=True)
class PaymentRefundResult:
    refund_id: str
    status: str


class PaymentGatewayPort(ABC):
    """Wallet/payment service — authorize before seat commit, capture/refund on outcome."""

    @abstractmethod
    async def authorize_payment(
        self, request: PaymentAuthorizationRequest
    ) -> PaymentAuthorizationResult:
        """Reserve funds; must be idempotent per idempotency_key."""

    @abstractmethod
    async def refund_payment(
        self, request: PaymentRefundRequest
    ) -> PaymentRefundResult:
        """Used when cancelling a paid ticket after capture."""


class ShowtimeSeatAssertionPort(ABC):
    """Billboard/showtime service (gRPC) — source of truth for concurrent seat rules."""

    @abstractmethod
    async def assert_seats_available_for_purchase(
        self, showtime_id: int, showtime_seat_ids: list[int]
    ) -> None:
        """Raise a domain error if any seat cannot be sold (sold elsewhere, hold, etc.)."""
