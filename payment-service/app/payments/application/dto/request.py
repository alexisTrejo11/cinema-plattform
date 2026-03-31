from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator

class PaymentRequestBase(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Unique identifier of the user account",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    
    amount: float = Field(
        ...,
        gt=0,
        description="Positive payment amount in specified currency",
        examples=[29.99]
    )
    
    currency: str = Field(
        default="USD",
        pattern="^[A-Z]{3}$",
        description="ISO 4217 currency code (3 uppercase letters)",
        examples=["USD", "EUR"]
    )
    
    wallet_id: Optional[UUID] = Field(
        default=None,
        description="Optional wallet identifier for wallet payments",
        examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    
    payment_method: str = Field(
        default="credit_card",
        pattern="^(credit_card|wallet|bank_transfer|cash)$",
        description="Selected payment method",
        examples=["credit_card"]
    )
    

class PayTicketRequest(PaymentRequestBase):
    """
    Request model for ticket payment processing.
    
    Attributes:
        user_id: Unique identifier of the user making the payment
        ticket_id: ticket ID to be paid
        amount: Total payment amount (must be positive)
        currency: Currency code in ISO 4217 format (default: USD)
        wallet_id: Optional wallet identifier for wallet payments
        payment_method: Payment method selected by user
    """
    model_config = ConfigDict(
        extra='forbid',
        frozen=False,
        str_strip_whitespace=True,
        validate_default=True,
        json_schema_extra={
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "ticket_id": "TICK-001",
                "amount": 29.99,
                "currency": "USD",
                "payment_method": "credit_card",
            }
        }
    )

    ticket_id: str = Field(
        ...,
        description="ticket identifiers to process",
        examples=["TICK-001"]
    )


class ProductItemRequest(BaseModel):
    product_id : str = Field(
        ...,
        description="product identifiers to process",
        examples=["PROD-001"]
    )
    product_quantity : int = Field(
        ...,
        gt=0,
        description="Positive product quantity in specified item",
        examples=[3]
    )


class PayProductsRequest(PaymentRequestBase):
    """
    Request model for ticket payment processing.
    
    Attributes:
        user_id: Unique identifier of the user making the payment
        ticket_id: ticket ID to be paid
        amount: Total payment amount (must be positive)
        currency: Currency code in ISO 4217 format (default: USD)
        wallet_id: Optional wallet identifier for wallet payments
        payment_method: Payment method selected by user
    """
    model_config = ConfigDict(
        extra='forbid',
        frozen=False,
        str_strip_whitespace=True,
        validate_default=True,
        json_schema_extra={
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "ticket_id": "TICK-001",
                "amount": 29.99,
                "currency": "USD",
                "payment_method": "credit_card",
            }
        }
    )

    product_ids: List[ProductItemRequest] = Field(
        ...,
        min_length=1
    )
    


