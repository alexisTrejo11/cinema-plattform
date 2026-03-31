from app.domain.entities.payment import Payment
from app.domain.value_objects import PaymentId, Money
from app.domain.repository.payment_repository import PaymentRepository
from app.application.interfaces import EventPublisher, PaymentGateway, NotificationService, WalletRepository
from app.domain.excpetions import PaymentNotRefundableException
from .command import RefundPaymentCommand
from .result import RefundPaymentResult

class RefundPaymentCommandHandler:
    """Handler for refunding payment commands."""
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
    
    async def handle(self, command: RefundPaymentCommand) -> RefundPaymentResult:
        """
        Handle payment refund command.
        
        Args:
            command: Payment refund command
            
        Returns:
            Payment refund result
            
        Raises:
            PaymentNotRefundableException: If payment cannot be refunded
            InvalidPaymentAmountException: If refund amount is invalid
        """
        try:
            # 1. Get payment from repository
            payment_id = PaymentId.from_string(str(command.payment_id))
            payment = await self.payment_repository.get_by_id(payment_id)
            
            if not payment:
                raise ValueError(f"Payment {command.payment_id} not found")
            
            # 2. Determine refund amount
            if command.refund_amount:
                refund_amount = Money.from_float(
                    command.refund_amount, 
                    payment.amount.currency
                )
            else:
                # Full refund of remaining refundable amount
                refund_amount = payment.get_remaining_refundable_amount()
            
            # 3. Validate refund is possible
            if not payment.can_be_refunded():
                raise PaymentNotRefundableException(
                    str(payment.id), 
                    "Payment is not in a refundable state"
                )
            
            # 4. Process refund based on original payment method
            if payment.payment_method.value == 'wallet':
                result = await self._process_wallet_refund(payment, refund_amount, command)
            else:
                result = await self._process_external_refund(payment, refund_amount, command)
            
            # 5. Apply refund to payment domain entity
            payment.refund(
                refund_amount=refund_amount,
                reason=command.reason,
                transaction_reference=result.get('transaction_id')
            )
            
            # 6. Save payment to repository
            saved_payment = await self.payment_repository.save(payment)
            
            # 7. Publish domain events
            await self._publish_events(payment)
            
            # 8. Send notifications
            await self._send_notifications(payment, result, refund_amount)
            
            return RefundPaymentResult(
                payment_id=saved_payment.id.value,
                refund_amount=refund_amount.to_float(),
                status=saved_payment.status.value,
                message="Payment refunded successfully",
                transaction_reference=result.get('transaction_id'),
                refunded_to_wallet=result.get('refunded_to_wallet', False)
            )
            
        except Exception as e:
            return RefundPaymentResult(
                payment_id=command.payment_id,
                refund_amount=command.refund_amount or 0.0,
                status="failed",
                message=f"Refund failed: {str(e)}"
            )
    
    async def _process_wallet_refund(
        self, 
        payment: Payment, 
        refund_amount: Money,
        command: RefundPaymentCommand
    ) -> dict:
        """Process refund back to user's wallet."""
        # Get user's wallet
        wallet = await self.wallet_repository.get_by_user_id(payment.user_id)
        if not wallet:
            raise ValueError("User wallet not found for refund")
        
        # Credit the refund amount to wallet
        transaction_id = wallet.credit(
            amount=refund_amount,
            description=f"Refund for payment {payment.id}: {command.reason}",
            reference_id=str(payment.id)
        )
        
        # Save wallet
        await self.wallet_repository.save(wallet)
        
        # Publish wallet events
        wallet_events = wallet.get_events()
        for event in wallet_events:
            await self.event_publisher.publish(event)
        wallet.clear_events()
        
        return {
            'transaction_id': str(transaction_id),
            'wallet_id': str(wallet.id),
            'method': 'wallet',
            'refunded_to_wallet': True
        }
    
    async def _process_external_refund(
        self, 
        payment: Payment, 
        refund_amount: Money,
        command: RefundPaymentCommand
    ) -> dict:
        """Process refund through external gateway."""
        
        # Check if user wants refund to wallet instead of original method
        if command.refund_to_wallet:
            return await self._process_wallet_refund(payment, refund_amount, command)
        
        # Process refund through external gateway
        if payment.external_reference:
            gateway_result = await self.payment_gateway.refund_payment(
                transaction_id=payment.external_reference.reference_id,
                amount=refund_amount.to_float(),
                reason=command.reason
            )
        else:
            raise ValueError("No external reference found for payment refund")
        
        # Check gateway result
        if gateway_result.get('status') != 'success':
            raise Exception(f"Gateway refund failed: {gateway_result.get('error')}")
        
        return {
            'transaction_id': gateway_result.get('refund_id'),
            'gateway_response': gateway_result,
            'method': payment.payment_method.value,
            'refunded_to_wallet': False
        }
    
    async def _publish_events(self, payment: Payment) -> None:
        """Publish all domain events from the payment."""
        events = payment.get_events()
        if events:
            await self.event_publisher.publish_batch(events)
            payment.clear_events()
    
    async def _send_notifications(
        self, 
        payment: Payment, 
        refund_result: dict,
        refund_amount: Money
    ) -> None:
        """Send refund confirmation notifications."""
        try:
            await self.notification_service.send_payment_confirmation(
                user_id=payment.user_id.value,
                payment_details={
                    'payment_id': str(payment.id),
                    'refund_amount': refund_amount.to_float(),
                    'currency': refund_amount.currency.value,
                    'refund_reason': payment.refund_reason,
                    'transaction_reference': refund_result.get('transaction_id'),
                    'refunded_to_wallet': refund_result.get('refunded_to_wallet', False),
                    'notification_type': 'refund_confirmation'
                }
            )
        except Exception as e:
            # Log notification failure but don't fail the refund
            print(f"Failed to send refund notification: {e}")
