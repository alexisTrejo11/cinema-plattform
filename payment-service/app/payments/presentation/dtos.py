from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, List

from pydantic import BaseModel, ConfigDict, Field

from app.shared.core.pagination import PaginationMetadata
from app.payments.application.commands import ProcessPayCommand
from app.payments.domain.entities import Payment
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.value_objects import (
    PaymentMethodType,
    PaymentProvider,
)

if TYPE_CHECKING:
    from app.payments.domain.entities.payment_method import PaymentMethod


class PaymentMethodResponse(BaseModel):
    """Public catalog entry returned by payment-method APIs (not saved card data)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "a1b2c3d4-e89b-12d3-a456-426614174000",
                "name": "Credit or debit card",
                "provider": "stripe",
                "type": "card",
                "stripe_code": "card",
                "is_active": True,
                "min_amount": 0.0,
                "created_at": "2026-03-31T12:00:00Z",
                "updated_at": "2026-03-31T12:00:00Z",
                "deleted_at": None,
            }
        }
    )

    id: str = Field(..., description="Stable id for this catalog row (UUID).")
    name: str = Field(..., description="Customer-facing label.")
    provider: PaymentProvider = Field(..., description="PSP / provider.")
    type: PaymentMethodType = Field(..., description="Method category.")
    stripe_code: str = Field(
        ...,
        description="Stripe PaymentMethod type / code (e.g. `card`, `oxxo`).",
    )
    is_active: bool = Field(
        ..., description="Whether the method is offered at checkout."
    )
    min_amount: float = Field(
        ...,
        ge=0,
        description="Minimum payable amount allowed for this method.",
    )
    created_at: datetime = Field(..., description="Row creation time (UTC).")
    updated_at: datetime = Field(..., description="Last update time (UTC).")
    deleted_at: Optional[datetime] = Field(
        None,
        description="When soft-deleted; `null` while active or restored.",
    )

    @classmethod
    def from_entity(cls, payment_method: "PaymentMethod") -> "PaymentMethodResponse":
        return cls(
            id=str(payment_method.id),
            name=payment_method.name,
            provider=payment_method.provider,
            type=payment_method.type,
            stripe_code=payment_method.stripe_code,
            is_active=payment_method.is_active,
            min_amount=payment_method.min_amount,
            created_at=payment_method.created_at,
            updated_at=payment_method.updated_at,
            deleted_at=payment_method.deleted_at,
        )


class UpdatePaymentMethodRequest(BaseModel):
    """Request body for `PUT /payment/methods/{id}`; path id is authoritative."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Credit or debit card (Visa, Mastercard)",
                "is_active": True,
                "min_amount": 1.0,
            }
        }
    )

    name: Optional[str] = Field(None, description="New display name.")
    provider: Optional[PaymentProvider] = Field(None, description="New provider.")
    type: Optional[PaymentMethodType] = Field(None, description="New category.")
    stripe_code: Optional[str] = Field(None, description="New Stripe type code.")
    is_active: Optional[bool] = Field(None, description="Enable or disable.")
    min_amount: Optional[float] = Field(
        None,
        ge=0,
        description="New minimum amount.",
    )


class PaymentResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: str
    payment_method: str
    payment_type: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    stripe_payment_intent_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_entity(cls, payment: Payment) -> "PaymentResponse":
        return cls(
            id=str(payment.id.value),
            user_id=str(payment.user_id.value),
            amount=payment.amount.to_float(),
            currency=payment.amount.currency.value,
            status=payment.status.value,
            payment_method=payment.payment_method.value,
            payment_type=payment.payment_type.value,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            completed_at=payment.completed_at,
            stripe_payment_intent_id=payment.stripe_payment_intent_id,
            metadata=(
                payment.metadata.model_dump(mode="json") if payment.metadata else {}
            ),
        )


class PaymentPaginatedResponse(BaseModel):
    items: List[PaymentResponse] = Field(
        default_factory=list, description="List of payments."
    )
    metadata: PaginationMetadata = Field(..., description="Page metadata.")


class PaymentSummaryResponse(BaseModel):
    total_payments: int
    completed_payments: int
    failed_payments: int
    total_paid_amount: float
    total_refunded_amount: float
    currency: str


class ReceiptResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str
    issued_at: datetime
    receipt_url: str


class InitiatePaymentRequest(BaseModel):
    payment_id: str = Field(..., description="Existing payment intent ID.")


class InitiatePaymentResponse(BaseModel):
    payment_id: str
    status: str
    stripe_payment_intent_id: str
    client_secret: str


class CancelPaymentRequest(BaseModel):
    reason: str = Field("Cancelled by user", description="Reason for cancellation.")


class RefundRequest(BaseModel):
    reason: str = Field(..., description="Refund reason.")
    refund_amount: Optional[float] = Field(
        None,
        gt=0,
        description="Optional partial refund amount. Full remaining amount when omitted.",
    )


class StaffRefundRequest(BaseModel):
    reason: str = Field(..., description="Operational reason for staff refund.")


class StoredPaymentMethodResponse(BaseModel):
    id: str
    user_id: str
    last4: str
    brand: str
    is_default: bool
    created_at: datetime


class TicketPurchaseRequest(BaseModel):
    """
    Placeholder payload for ticket purchases.
    You can refine fields once billboard contracts are finalized.
    """

    show_id: str
    showtime_id: str
    seats: list[str]
    total_amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str = "stripe"
    notes: Optional[str] = None

    def to_command(self, user_id: str) -> ProcessPayCommand:
        return ProcessPayCommand(
            product_id="00000000-0000-0000-0000-000000000001",
            user_id=user_id,
            amount=self.total_amount,
            payment_method=self.payment_method,
            payment_type="ticket_purchase",
            currency=self.currency,
            metadata={
                "show_id": self.show_id,
                "showtime_id": self.showtime_id,
                "seat_numbers": self.seats,
                "notes": self.notes,
            },
        )


class ConcessionsPurchaseRequest(BaseModel):
    order_id: str
    items: list[dict[str, Any]]
    total_amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str = "stripe"

    def to_command(self, user_id: str) -> ProcessPayCommand:
        return ProcessPayCommand(
            product_id="00000000-0000-0000-0000-000000000002",
            user_id=user_id,
            amount=self.total_amount,
            payment_method=self.payment_method,
            payment_type="food_purchase",
            currency=self.currency,
            metadata={"order_id": self.order_id, "food_items": self.items},
        )


class MerchandisePurchaseRequest(BaseModel):
    order_id: str
    items: list[dict[str, Any]]
    total_amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str = "stripe"

    def to_command(self, user_id: str) -> ProcessPayCommand:
        return ProcessPayCommand(
            product_id="00000000-0000-0000-0000-000000000003",
            user_id=user_id,
            amount=self.total_amount,
            payment_method=self.payment_method,
            payment_type="merchandise_purchase",
            currency=self.currency,
            metadata={"order_id": self.order_id, "items": self.items},
        )


class SubscriptionPurchaseRequest(BaseModel):
    plan_id: str
    period: str = "monthly"
    total_amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str = "stripe"

    def to_command(self, user_id: str) -> ProcessPayCommand:
        return ProcessPayCommand(
            product_id="00000000-0000-0000-0000-000000000004",
            user_id=user_id,
            amount=self.total_amount,
            payment_method=self.payment_method,
            payment_type="subscription",
            currency=self.currency,
            metadata={"plan_id": self.plan_id, "period": self.period},
        )


class WalletCreditPurchaseRequest(BaseModel):
    wallet_id: Optional[str] = None
    total_amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str = "stripe"

    def to_command(self, user_id: str) -> ProcessPayCommand:
        return ProcessPayCommand(
            product_id="00000000-0000-0000-0000-000000000005",
            user_id=user_id,
            amount=self.total_amount,
            payment_method=self.payment_method,
            payment_type="wallet_topup",
            currency=self.currency,
            wallet_id=self.wallet_id,
            metadata={"wallet_id": self.wallet_id},
        )


class AdminPaymentSearchQuery(BaseModel):
    """Query string for `GET .../admin/payments` — maps to `PaymentListCriteria`."""

    user_id: Optional[str] = None
    status: Optional[str] = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    def to_criteria(self) -> PaymentListCriteria:
        return PaymentListCriteria(
            user_id=self.user_id,
            status=self.status,
            limit=self.limit,
            offset=self.offset,
        )


class AdminPaginationQuery(BaseModel):
    """Limit/offset only (e.g. admin transaction list)."""

    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    def to_criteria(self) -> PaymentListCriteria:
        return PaymentListCriteria.paginate(limit=self.limit, offset=self.offset)


class AdminOverrideStatusRequest(BaseModel):
    status: str = Field(..., description="Target payment status.")


class AdminRefundRequest(BaseModel):
    reason: str
    refund_amount: Optional[float] = None


class AdminVoidRequest(BaseModel):
    reason: str = "Voided by admin"


class ReverseTransactionRequest(BaseModel):
    reason: str


class StripeWebhookRequest(BaseModel):
    event_type: str
    payload: dict[str, Any]
