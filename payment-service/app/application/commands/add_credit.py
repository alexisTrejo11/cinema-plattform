from pydantic import BaseModel, Field, PositiveFloat, UUID4
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal

from app.domain.entities.wallet import Wallet
from app.domain.value_objects import (
    UserId, Money, Currency, WalletId
)
from app.application.interfaces import (
    EventPublisher, WalletRepository, NotificationService
)
from app.shared.value_objects import PositiveDecimal, TransactionReference, TransactionSource


class AddCreditCommand(BaseModel):
    """Command to add credit to a user's account"""
    user_id: UUID4 = Field(..., description="ID of the user to credit.")
    amount: PositiveFloat = Field(..., gt=0, description="Amount to credit.")
    currency: str = Field("USD", max_length=3, min_length=3, description="Currency code.")
    reference_id: str = Field(..., max_length=50, description="External reference ID.")
    source: str = Field("system", description="Source of the credit.")
    description: str = Field(..., max_length=500, description="Description of the credit.")
    wallet_id: Optional[UUID4] = Field(None, description="Specific wallet ID (optional).")
    expires_at: Optional[datetime] = Field(None, description="Credit expiration date.")
    idempotency_key: Optional[UUID4] = Field(None, description="Idempotency key.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "amount": 50.00,
                "currency": "USD",
                "reference_id": "pay_123456",
                "source": "payment",
                "description": "Credit from PayPal top-up",
                "expires_at": "2024-12-31T23:59:59Z",
                "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }


class AddCreditResult(BaseModel):
    """Result of adding credit to wallet."""
    wallet_id: UUID
    transaction_id: UUID
    user_id: UUID
    amount: float
    currency: str
    new_balance: float
    status: str
    message: str


class AddCreditCommandHandler:
    """Handler for adding credit to user wallets."""
    
    def __init__(
        self,
        wallet_repository: WalletRepository,
        event_publisher: EventPublisher,
        notification_service: NotificationService
    ):
        self.wallet_repository = wallet_repository
        self.event_publisher = event_publisher
        self.notification_service = notification_service
    
    async def handle(self, command: AddCreditCommand) -> AddCreditResult:
        """
        Handle add credit command.
        
        Args:
            command: Add credit command
            
        Returns:
            Add credit result
            
        Raises:
            ValueError: If wallet not found or invalid parameters
            InvalidWalletOperationException: If credit operation fails
        """
        try:
            # 1. Create domain objects from command
            user_id = UserId.from_string(str(command.user_id))
            amount = Money.from_float(command.amount, Currency(command.currency))
            
            # 2. Get or create wallet
            if command.wallet_id:
                # Use specific wallet
                wallet_id = WalletId.from_string(str(command.wallet_id))
                wallet = await self.wallet_repository.get_by_id(wallet_id)
                if not wallet:
                    raise ValueError(f"Wallet {command.wallet_id} not found")
            else:
                # Get user's default wallet
                wallet = await self.wallet_repository.get_by_user_id(user_id)
                if not wallet:
                    # Create new wallet for user
                    wallet = Wallet.create(
                        user_id=user_id,
                        currency=Currency(command.currency)
                    )
                    wallet = await self.wallet_repository.save(wallet)
            
            # 3. Validate wallet currency matches credit currency
            if wallet.currency != Currency(command.currency):
                raise ValueError(
                    f"Wallet currency {wallet.currency} does not match credit currency {command.currency}"
                )
            
            # 4. Add credit to wallet
            transaction_id = wallet.credit(
                amount=amount,
                description=command.description,
                reference_id=command.reference_id
            )
            
            # 5. Save wallet
            saved_wallet = await self.wallet_repository.save(wallet)
            
            # 6. Publish domain events
            await self._publish_events(wallet)
            
            # 7. Send notifications
            await self._send_notifications(wallet, amount, transaction_id)
            
            return AddCreditResult(
                wallet_id=saved_wallet.id.value,
                transaction_id=transaction_id.value,
                user_id=saved_wallet.user_id.value,
                amount=amount.to_float(),
                currency=amount.currency.value,
                new_balance=saved_wallet.balance.to_float(),
                status="success",
                message="Credit added successfully"
            )
            
        except Exception as e:
            return AddCreditResult(
                wallet_id=command.wallet_id or UUID(int=0),
                transaction_id=UUID(int=0),
                user_id=command.user_id,
                amount=command.amount,
                currency=command.currency,
                new_balance=0.0,
                status="failed",
                message=f"Credit addition failed: {str(e)}"
            )
    
    async def _publish_events(self, wallet: Wallet) -> None:
        """Publish all domain events from the wallet."""
        events = wallet.get_events()
        if events:
            await self.event_publisher.publish_batch(events)
            wallet.clear_events()
    
    async def _send_notifications(
        self, 
        wallet: Wallet, 
        amount: Money,
        transaction_id
    ) -> None:
        """Send credit confirmation notifications."""
        try:
            await self.notification_service.send_payment_confirmation(
                user_id=wallet.user_id.value,
                payment_details={
                    'wallet_id': str(wallet.id),
                    'transaction_id': str(transaction_id),
                    'amount': amount.to_float(),
                    'currency': amount.currency.value,
                    'new_balance': wallet.balance.to_float(),
                    'notification_type': 'credit_added'
                }
            )
        except Exception as e:
            # Log notification failure but don't fail the credit operation
            print(f"Failed to send credit notification: {e}")
