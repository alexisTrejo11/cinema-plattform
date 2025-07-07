from pydantic import BaseModel, Field, PositiveFloat, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from app.domain.entities.payment import Payment
from app.domain.value_objects import (
    UserId, Money, PaymentMethod, PaymentType, PaymentMetadata, Currency
)
from app.domain.repository.payment_repository import PaymentRepository
from app.application.interfaces import (
    EventPublisher, PaymentGateway, NotificationService, WalletRepository
)
from app.domain.excpetions import (
    PaymentAlreadyProcessedException, InvalidPaymentAmountException
)


class ProcessPayCommand(BaseModel):
    """
    Command to initiate payment processing.
    """
    product_id: UUID4 = Field(..., description="Unique ID of the product to purchase.")
    user_id: UUID4 = Field(..., description="ID of the user making the purchase.")
    amount: PositiveFloat = Field(..., gt=0, description="Total purchase amount.")
    payment_method: str = Field(..., pattern="^(wallet|credit_card|debit_card|paypal|stripe)$", description="Payment method.")
    payment_type: str = Field(..., pattern="^(ticket_purchase|food_purchase|merchandise_purchase|wallet_topup)$", description="Type of payment.")
    wallet_id: Optional[UUID4] = Field(None, description="Wallet ID if payment method is 'wallet'.")
    currency: str = Field("USD", max_length=3, min_length=3, description="Currency code (e.g., 'MXN', 'USD').")
    correlation_id: Optional[UUID4] = Field(None, description="ID for correlating events.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional payment metadata.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

    class Config:
        schema_extra = {
            "example": {
                "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                "amount": 150.75,
                "payment_method": "wallet",
                "payment_type": "ticket_purchase",
                "wallet_id": "fedcba98-7654-3210-fedc-ba9876543210",
                "currency": "USD"
            }
        }


class ProcessPaymentResult(BaseModel):
    """Result of payment processing."""
    payment_id: UUID
    status: str
    message: str
    transaction_reference: Optional[str] = None


class ProcessPaymentCommandHandler:
    """Handler for processing payment commands."""
    
    def __init__(
        self,
        payment_repository: PaymentRepository,
        wallet_repository: WalletRepository,
        event_publisher: EventPublisher,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService
    ):
        self.payment_repository = payment_repository
        self.wallet_repository = wallet_repository
        self.event_publisher = event_publisher
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
    
    async def handle(self, command: ProcessPayCommand) -> ProcessPaymentResult:
        """
        Handle payment processing command.
        
        Args:
            command: Payment processing command
            
        Returns:
            Payment processing result
            
        Raises:
            InvalidPaymentAmountException: If payment amount is invalid
            InsufficientFundsException: If wallet has insufficient funds
            PaymentAlreadyProcessedException: If payment is already processed
        """
        try:
            # 1. Create domain objects from command
            user_id = UserId.from_string(str(command.user_id))
            amount = Money.from_float(command.amount, Currency(command.currency))
            payment_method = PaymentMethod(command.payment_method)
            payment_type = PaymentType(command.payment_type)
            
            # Create payment metadata
            payment_metadata = None
            if command.metadata:
                payment_metadata = PaymentMetadata(
                    ticket_ids=command.metadata.get('ticket_ids'),
                    showtime_id=command.metadata.get('showtime_id'),
                    seat_numbers=command.metadata.get('seat_numbers'),
                    food_items=command.metadata.get('food_items'),
                    pickup_location=command.metadata.get('pickup_location'),
                    special_instructions=command.metadata.get('special_instructions')
                )
            
            # 2. Create payment domain entity
            payment = Payment.create(
                user_id=user_id,
                amount=amount,
                payment_method=payment_method,
                payment_type=payment_type,
                metadata=payment_metadata
            )
            
            # 3. Start payment processing
            payment.start_processing()
            
            # 4. Handle payment method-specific logic
            if payment_method == PaymentMethod.WALLET:
                result = await self._process_wallet_payment(payment, command.wallet_id)
            else:
                result = await self._process_external_payment(payment, command)
            
            # 5. Save payment to repository
            saved_payment = await self.payment_repository.save(payment)
            
            # 6. Publish domain events
            await self._publish_events(payment)
            
            # 7. Send notifications
            await self._send_notifications(payment, result)
            
            return ProcessPaymentResult(
                payment_id=saved_payment.id.value,
                status=saved_payment.status.value,
                message="Payment processed successfully",
                transaction_reference=result.get('transaction_id')
            )
            
        except Exception as e:
            # Handle payment failure
            if 'payment' in locals():
                payment.fail(str(e), error_code=type(e).__name__)
                await self.payment_repository.save(payment)
                await self._publish_events(payment)
                await self._send_notifications(payment, {'error': str(e)})
            
            return ProcessPaymentResult(
                payment_id=payment.id.value if 'payment' in locals() else UUID(int=0),
                status="failed",
                message=f"Payment failed: {str(e)}"
            )
    
    async def _process_wallet_payment(
        self, 
        payment: Payment, 
        wallet_id: Optional[UUID]
    ) -> Dict[str, Any]:
        """Process payment using wallet funds."""
        if not wallet_id:
            # Get user's wallet
            wallet = await self.wallet_repository.get_by_user_id(payment.user_id)
            if not wallet:
                raise ValueError("User does not have a wallet")
        else:
            # Use specific wallet
            from app.domain.value_objects import WalletId
            wallet = await self.wallet_repository.get_by_id(
                WalletId.from_string(str(wallet_id))
            )
            if not wallet:
                raise ValueError("Wallet not found")
        
        # Check if wallet can debit the amount
        if not wallet.can_debit(payment.amount):
            from app.domain.excpetions import InsufficientFundsException
            raise InsufficientFundsException(
                wallet.get_available_balance().to_float(),
                payment.amount.to_float()
            )
        
        # Debit from wallet
        transaction_id = wallet.debit(
            amount=payment.amount,
            description=f"Payment for {payment.payment_type.value}",
            reference_id=str(payment.id)
        )
        
        # Save wallet
        await self.wallet_repository.save(wallet)
        
        # Complete payment
        payment.complete(transaction_reference=str(transaction_id))
        
        # Publish wallet events
        wallet_events = wallet.get_events()
        for event in wallet_events:
            await self.event_publisher.publish(event)
        wallet.clear_events()
        
        return {
            'transaction_id': str(transaction_id),
            'wallet_id': str(wallet.id),
            'method': 'wallet'
        }
    
    async def _process_external_payment(
        self, 
        payment: Payment, 
        command: ProcessPayCommand
    ) -> Dict[str, Any]:
        """Process payment using external gateway."""
        # Prepare payment data for gateway
        gateway_metadata = {
            'payment_id': str(payment.id),
            'user_id': str(payment.user_id),
            'payment_type': payment.payment_type.value,
            'correlation_id': str(command.correlation_id) if command.correlation_id else None
        }
        
        if command.metadata:
            gateway_metadata.update(command.metadata)
        
        # Process through external gateway
        gateway_result = await self.payment_gateway.process_payment(
            amount=payment.amount.to_float(),
            currency=payment.amount.currency.value,
            payment_method=payment.payment_method.value,
            metadata=gateway_metadata
        )
        
        # Check gateway result
        if gateway_result.get('status') == 'success':
            payment.complete(transaction_reference=gateway_result.get('transaction_id'))
        else:
            payment.fail(
                reason=gateway_result.get('error', 'Unknown gateway error'),
                error_code=gateway_result.get('error_code')
            )
        
        return gateway_result
    
    async def _publish_events(self, payment: Payment) -> None:
        """Publish all domain events from the payment."""
        events = payment.get_events()
        if events:
            await self.event_publisher.publish_batch(events)
            payment.clear_events()
    
    async def _send_notifications(
        self, 
        payment: Payment, 
        processing_result: Dict[str, Any]
    ) -> None:
        """Send appropriate notifications based on payment status."""
        try:
            if payment.status.value == 'completed':
                await self.notification_service.send_payment_confirmation(
                    user_id=payment.user_id.value,
                    payment_details={
                        'payment_id': str(payment.id),
                        'amount': payment.amount.to_float(),
                        'currency': payment.amount.currency.value,
                        'payment_type': payment.payment_type.value,
                        'transaction_reference': processing_result.get('transaction_id')
                    }
                )
            elif payment.status.value in ['failed', 'cancelled']:
                await self.notification_service.send_payment_failure(
                    user_id=payment.user_id.value,
                    failure_details={
                        'payment_id': str(payment.id),
                        'amount': payment.amount.to_float(),
                        'currency': payment.amount.currency.value,
                        'failure_reason': payment.failure_reason,
                        'error_details': processing_result.get('error')
                    }
                )
        except Exception as e:
            # Log notification failure but don't fail the payment
            print(f"Failed to send notification: {e}")
