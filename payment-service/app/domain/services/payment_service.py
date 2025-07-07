from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from ..entities import Payment, Wallet
from ..value_objects import (
    Money, PaymentType, PaymentMethod, PaymentStatus, UserId, Currency
)
from ..excpetions import (
    PaymentNotRefundableException, InsufficientFundsException,
    InvalidPaymentAmountException
)


class PaymentDomainService:
    """
    Domain service for complex payment operations.
    
    Handles business logic that requires coordination between
    Payment and Wallet aggregates or external considerations.
    """
    
    MAX_REFUND_PERCENTAGE = Decimal('1.0')  # 100%
    PARTIAL_REFUND_FEE_PERCENTAGE = Decimal('0.03')  # 3%
    BULK_PAYMENT_DISCOUNT_THRESHOLD = 5  # Number of tickets
    BULK_PAYMENT_DISCOUNT_PERCENTAGE = Decimal('0.05')  # 5%
    
    def calculate_payment_fees(
        self,
        amount: Money,
        payment_method: PaymentMethod,
        payment_type: PaymentType
    ) -> Money:
        """
        Calculate fees for a payment based on method and type.
        
        Args:
            amount: Base payment amount
            payment_method: Method of payment
            payment_type: Type of payment
            
        Returns:
            Fee amount to be added to base payment
        """
        # Base fee calculation based on payment method
        fee_percentage = Decimal('0.0')
        
        if payment_method == PaymentMethod.CREDIT_CARD:
            fee_percentage = Decimal('0.029')  # 2.9%
        elif payment_method == PaymentMethod.DEBIT_CARD:
            fee_percentage = Decimal('0.015')  # 1.5%
        elif payment_method == PaymentMethod.PAYPAL:
            fee_percentage = Decimal('0.034')  # 3.4%
        elif payment_method == PaymentMethod.WALLET:
            fee_percentage = Decimal('0.0')  # No fee for wallet
        elif payment_method == PaymentMethod.BANK_TRANSFER:
            fee_percentage = Decimal('0.01')  # 1%
        
        # Additional fees based on payment type
        if payment_type == PaymentType.TICKET_PURCHASE:
            # Small processing fee for tickets
            fee_percentage += Decimal('0.005')  # 0.5%
        elif payment_type == PaymentType.FOOD_PURCHASE:
            # No additional fee for food
            pass
        
        # Calculate fee amount
        fee_amount = amount.amount * fee_percentage
        return Money(fee_amount, amount.currency)
    
    def calculate_bulk_discount(
        self,
        base_amount: Money,
        item_count: int,
        payment_type: PaymentType
    ) -> Money:
        """
        Calculate bulk discount for large purchases.
        
        Args:
            base_amount: Base payment amount
            item_count: Number of items being purchased
            payment_type: Type of payment
            
        Returns:
            Discount amount to be subtracted from base amount
        """
        # Only apply bulk discount to ticket purchases
        if payment_type != PaymentType.TICKET_PURCHASE:
            return Money.zero(base_amount.currency)
        
        # Apply discount for bulk purchases
        if item_count >= self.BULK_PAYMENT_DISCOUNT_THRESHOLD:
            discount_amount = base_amount.amount * self.BULK_PAYMENT_DISCOUNT_PERCENTAGE
            return Money(discount_amount, base_amount.currency)
        
        return Money.zero(base_amount.currency)
    
    def calculate_refund_amount(
        self,
        payment: Payment,
        refund_percentage: Optional[Decimal] = None
    ) -> Money:
        """
        Calculate refund amount considering business rules.
        
        Args:
            payment: Payment to be refunded
            refund_percentage: Percentage to refund (default: 100%)
            
        Returns:
            Amount that can be refunded
            
        Raises:
            PaymentNotRefundableException: If refund is not allowed
        """
        if not payment.can_be_refunded():
            raise PaymentNotRefundableException(
                str(payment.id),
                "Payment is not in a refundable state"
            )
        
        # Default to full refund
        if refund_percentage is None:
            refund_percentage = self.MAX_REFUND_PERCENTAGE
        
        # Validate refund percentage
        if refund_percentage < 0 or refund_percentage > self.MAX_REFUND_PERCENTAGE:
            raise ValueError("Refund percentage must be between 0 and 100%")
        
        # Calculate base refund amount
        remaining_refundable = payment.get_remaining_refundable_amount()
        base_refund = remaining_refundable.multiply(refund_percentage)
        
        # Apply refund fees for partial refunds
        if refund_percentage < self.MAX_REFUND_PERCENTAGE:
            fee = base_refund.multiply(self.PARTIAL_REFUND_FEE_PERCENTAGE)
            return base_refund.subtract(fee)
        
        # For ticket refunds, check timing
        if payment.payment_type == PaymentType.TICKET_PURCHASE:
            refund_amount = self._apply_ticket_refund_policy(payment, base_refund)
            return refund_amount
        
        return base_refund
    
    def validate_wallet_payment(
        self,
        wallet: Wallet,
        amount: Money,
        include_fees: bool = True
    ) -> bool:
        """
        Validate if wallet can be used for payment.
        
        Args:
            wallet: User's wallet
            amount: Payment amount
            include_fees: Whether to include potential fees
            
        Returns:
            True if payment is possible, False otherwise
        """
        if not wallet.is_usable():
            return False
        
        if amount.currency != wallet.currency:
            return False
        
        # Calculate total amount including potential fees
        total_amount = amount
        if include_fees:
            # Assume no fees for wallet payments, but could add logic here
            pass
        
        return wallet.can_debit(total_amount)
    
    def suggest_payment_methods(
        self,
        user_id: UserId,
        amount: Money,
        payment_type: PaymentType,
        user_wallet: Optional[Wallet] = None
    ) -> List[PaymentMethod]:
        """
        Suggest appropriate payment methods for a user.
        
        Args:
            user_id: User making the payment
            amount: Payment amount
            payment_type: Type of payment
            user_wallet: User's wallet (if available)
            
        Returns:
            List of recommended payment methods
        """
        suggestions = []
        
        # Check wallet if available
        if user_wallet and self.validate_wallet_payment(user_wallet, amount):
            suggestions.append(PaymentMethod.WALLET)
        
        # Add standard payment methods
        suggestions.extend([
            PaymentMethod.STRIPE,  # Preferred for credit cards
            PaymentMethod.PAYPAL,
            PaymentMethod.CREDIT_CARD,
            PaymentMethod.DEBIT_CARD
        ])
        
        # For large amounts, suggest bank transfer
        if amount.to_float() > 100.0:
            suggestions.append(PaymentMethod.BANK_TRANSFER)
        
        return suggestions
    
    def calculate_payment_expiry(
        self,
        payment_type: PaymentType,
        payment_method: PaymentMethod
    ) -> datetime:
        """
        Calculate when a payment should expire.
        
        Args:
            payment_type: Type of payment
            payment_method: Method of payment
            
        Returns:
            Expiry datetime
        """
        base_expiry_minutes = 30  # Default
        
        # Adjust based on payment method
        if payment_method == PaymentMethod.BANK_TRANSFER:
            base_expiry_minutes = 60 * 24  # 24 hours for bank transfers
        elif payment_method == PaymentMethod.WALLET:
            base_expiry_minutes = 15  # Shorter for wallet payments
        
        # Adjust based on payment type
        if payment_type == PaymentType.TICKET_PURCHASE:
            # Give more time for ticket purchases
            base_expiry_minutes += 15
        
        return datetime.utcnow() + timedelta(minutes=base_expiry_minutes)
    
    def validate_payment_amount_limits(
        self,
        amount: Money,
        payment_type: PaymentType,
        user_id: UserId
    ) -> bool:
        """
        Validate payment amount against business limits.
        
        Args:
            amount: Payment amount to validate
            payment_type: Type of payment
            user_id: User making the payment
            
        Returns:
            True if amount is within limits, False otherwise
        """
        # Minimum amount validation
        min_amount = Decimal('0.50')  # $0.50 minimum
        if amount.amount < min_amount:
            return False
        
        # Maximum amount validation by type
        max_amounts = {
            PaymentType.TICKET_PURCHASE: Decimal('1000.00'),
            PaymentType.FOOD_PURCHASE: Decimal('200.00'),
            PaymentType.MERCHANDISE_PURCHASE: Decimal('500.00'),
            PaymentType.WALLET_TOPUP: Decimal('2000.00'),
            PaymentType.SUBSCRIPTION: Decimal('100.00')
        }
        
        max_amount = max_amounts.get(payment_type, Decimal('1000.00'))
        if amount.amount > max_amount:
            return False
        
        return True
    
    def _apply_ticket_refund_policy(
        self,
        payment: Payment,
        base_refund: Money
    ) -> Money:
        """
        Apply specific refund policy for ticket purchases.
        
        Args:
            payment: Ticket payment
            base_refund: Base refund amount
            
        Returns:
            Adjusted refund amount based on policy
        """
        if not payment.completed_at:
            return base_refund
        
        # Get time since payment completion
        time_since_payment = datetime.utcnow() - payment.completed_at
        
        # Apply time-based refund policy
        if time_since_payment > timedelta(days=7):
            # After 7 days, 90% refund
            return base_refund.multiply(Decimal('0.9'))
        elif time_since_payment > timedelta(days=1):
            # After 1 day, 95% refund
            return base_refund.multiply(Decimal('0.95'))
        else:
            # Within 24 hours, full refund
            return base_refund
    
    def is_payment_suspicious(
        self,
        user_id: UserId,
        amount: Money,
        payment_method: PaymentMethod,
        recent_payments: List[Payment]
    ) -> bool:
        """
        Check if payment might be suspicious based on patterns.
        
        Args:
            user_id: User making the payment
            amount: Payment amount
            payment_method: Method of payment
            recent_payments: Recent payments by the user
            
        Returns:
            True if payment appears suspicious, False otherwise
        """
        # Check for unusual amounts
        if amount.to_float() > 500.0:
            return True
        
        # Check for rapid payments
        recent_count = len([
            p for p in recent_payments
            if p.created_at > datetime.utcnow() - timedelta(hours=1)
        ])
        
        if recent_count > 3:
            return True
        
        # Check for failed payment patterns
        recent_failures = len([
            p for p in recent_payments
            if p.status == PaymentStatus.FAILED and
            p.created_at > datetime.utcnow() - timedelta(hours=24)
        ])
        
        if recent_failures > 2:
            return True
        
        return False
