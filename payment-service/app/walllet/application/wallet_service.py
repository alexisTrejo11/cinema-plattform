"""
Wallet Domain Service

Implements complex wallet business logic including transfers,
balance calculations, and multi-wallet operations.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Tuple

from ...payment.domain.entities import Wallet, Transaction
from ...payment.domain.value_objects import (
    Money, Currency, TransactionType, WalletId, UserId, TransactionId
)
from ...payment.domain.excpetions import (
    InsufficientFundsException, InvalidWalletOperationException,
    WalletNotActiveException
)


class WalletDomainService:
    """
    Domain service for complex wallet operations.
    
    Handles business logic that spans multiple wallets or requires
    complex calculations and validations.
    """
    
    # Business rules constants
    TRANSFER_FEE_PERCENTAGE = Decimal('0.01')  # 1% transfer fee
    TRANSFER_FEE_MINIMUM = Decimal('0.50')    # Minimum transfer fee
    TRANSFER_FEE_MAXIMUM = Decimal('5.00')    # Maximum transfer fee
    DAILY_TRANSFER_LIMIT = Decimal('1000.00')  # Daily transfer limit
    
    def transfer_between_wallets(
        self,
        source_wallet: Wallet,
        target_wallet: Wallet,
        amount: Money,
        description: str,
        apply_fees: bool = True
    ) -> Tuple[TransactionId, TransactionId, Optional[TransactionId]]:
        """
        Transfer money between two wallets.
        
        Args:
            source_wallet: Wallet to transfer from
            target_wallet: Wallet to transfer to
            amount: Amount to transfer
            description: Transfer description
            apply_fees: Whether to apply transfer fees
            
        Returns:
            Tuple of (debit_transaction_id, credit_transaction_id, fee_transaction_id)
            
        Raises:
            WalletNotActiveException: If either wallet is not active
            InsufficientFundsException: If source wallet has insufficient funds
            InvalidWalletOperationException: If transfer violates business rules
        """
        # Validate wallets
        if not source_wallet.is_usable():
            raise WalletNotActiveException(str(source_wallet.id))
        
        if not target_wallet.is_usable():
            raise WalletNotActiveException(str(target_wallet.id))
        
        # Validate currency compatibility
        if source_wallet.currency != target_wallet.currency:
            raise InvalidWalletOperationException(
                "transfer",
                f"Currency mismatch: {source_wallet.currency} != {target_wallet.currency}"
            )
        
        if amount.currency != source_wallet.currency:
            raise InvalidWalletOperationException(
                "transfer",
                f"Amount currency {amount.currency} doesn't match wallet currency {source_wallet.currency}"
            )
        
        # Calculate fees
        transfer_fee = Money.zero(amount.currency)
        if apply_fees:
            transfer_fee = self.calculate_transfer_fee(amount)
        
        # Calculate total amount needed from source
        total_debit = amount.add(transfer_fee)
        
        # Check if source wallet has sufficient funds
        if not source_wallet.can_debit(total_debit):
            raise InsufficientFundsException(
                source_wallet.get_available_balance().to_float(),
                total_debit.to_float()
            )
        
        # Perform the transfer
        debit_transaction_id = source_wallet.debit(
            total_debit,
            f"Transfer to {target_wallet.id}: {description}",
            reference_id=f"transfer_{TransactionId.generate()}"
        )
        
        credit_transaction_id = target_wallet.credit(
            amount,
            f"Transfer from {source_wallet.id}: {description}",
            reference_id=f"transfer_{debit_transaction_id}"
        )
        
        fee_transaction_id = None
        if transfer_fee.is_positive():
            # Record fee transaction (in a real system, this might go to a fee collection wallet)
            fee_transaction_id = TransactionId.generate()
        
        return debit_transaction_id, credit_transaction_id, fee_transaction_id
    
    def calculate_transfer_fee(self, amount: Money) -> Money:
        """
        Calculate transfer fee based on amount.
        
        Args:
            amount: Transfer amount
            
        Returns:
            Fee amount
        """
        fee_amount = amount.amount * self.TRANSFER_FEE_PERCENTAGE
        
        # Apply minimum and maximum fee limits
        if fee_amount < self.TRANSFER_FEE_MINIMUM:
            fee_amount = self.TRANSFER_FEE_MINIMUM
        elif fee_amount > self.TRANSFER_FEE_MAXIMUM:
            fee_amount = self.TRANSFER_FEE_MAXIMUM
        
        return Money(fee_amount, amount.currency)
    
    def calculate_wallet_metrics(
        self,
        wallet: Wallet,
        transactions: List[Transaction],
        period_days: int = 30
    ) -> dict:
        """
        Calculate various metrics for a wallet.
        
        Args:
            wallet: Wallet to analyze
            transactions: Recent transactions
            period_days: Period for analysis in days
            
        Returns:
            Dictionary with wallet metrics
        """
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        recent_transactions = [
            t for t in transactions
            if t.created_at >= cutoff_date and not t.is_reversed
        ]
        
        # Calculate transaction counts by type
        credit_count = len([t for t in recent_transactions if t.is_credit()])
        debit_count = len([t for t in recent_transactions if t.is_debit()])
        refund_count = len([t for t in recent_transactions if t.is_refund()])
        
        # Calculate amounts by type
        total_credits = sum(
            (t.amount.to_float() for t in recent_transactions if t.is_credit()),
            0.0
        )
        total_debits = sum(
            (t.amount.to_float() for t in recent_transactions if t.is_debit()),
            0.0
        )
        total_refunds = sum(
            (t.amount.to_float() for t in recent_transactions if t.is_refund()),
            0.0
        )
        
        # Calculate average transaction amounts
        avg_credit = total_credits / credit_count if credit_count > 0 else 0.0
        avg_debit = total_debits / debit_count if debit_count > 0 else 0.0
        
        # Calculate net flow
        net_flow = total_credits - total_debits + total_refunds
        
        return {
            "current_balance": wallet.balance.to_float(),
            "available_balance": wallet.get_available_balance().to_float(),
            "period_days": period_days,
            "transaction_counts": {
                "credits": credit_count,
                "debits": debit_count,
                "refunds": refund_count,
                "total": len(recent_transactions)
            },
            "amounts": {
                "total_credits": total_credits,
                "total_debits": total_debits,
                "total_refunds": total_refunds,
                "net_flow": net_flow
            },
            "averages": {
                "credit_amount": avg_credit,
                "debit_amount": avg_debit
            },
            "status": wallet.status.value,
            "currency": wallet.currency.value
        }
    
    def validate_daily_limits(
        self,
        wallet: Wallet,
        amount: Money,
        transaction_type: TransactionType,
        today_transactions: List[Transaction]
    ) -> bool:
        """
        Validate if transaction is within daily limits.
        
        Args:
            wallet: Wallet for transaction
            amount: Transaction amount
            transaction_type: Type of transaction
            today_transactions: Transactions from today
            
        Returns:
            True if within limits, False otherwise
        """
        # Calculate today's total for the transaction type
        today_total = sum(
            t.amount.to_float() for t in today_transactions
            if t.transaction_type == transaction_type and not t.is_reversed
        )
        
        # Check against daily limits
        if transaction_type == TransactionType.DEBIT:
            daily_limit = self.DAILY_TRANSFER_LIMIT.to_float()
            if today_total + amount.to_float() > daily_limit:
                return False
        
        # Check wallet-specific limits if set
        if wallet.daily_limit:
            if today_total + amount.to_float() > wallet.daily_limit.to_float():
                return False
        
        return True
    
    def suggest_optimal_balance(
        self,
        wallet: Wallet,
        transactions: List[Transaction],
        target_days: int = 30
    ) -> Money:
        """
        Suggest optimal balance based on spending patterns.
        
        Args:
            wallet: Wallet to analyze
            transactions: Historical transactions
            target_days: Number of days to plan for
            
        Returns:
            Suggested optimal balance
        """
        # Analyze spending patterns
        cutoff_date = datetime.utcnow() - timedelta(days=90)  # 3 months of data
        recent_debits = [
            t for t in transactions
            if (t.is_debit() and t.created_at >= cutoff_date and 
                not t.is_reversed)
        ]
        
        if not recent_debits:
            # No spending history, suggest a conservative amount
            return Money.from_float(100.0, wallet.currency)
        
        # Calculate average daily spending
        total_spent = sum(t.amount.to_float() for t in recent_debits)
        days_analyzed = (datetime.utcnow() - cutoff_date).days
        daily_average = total_spent / days_analyzed if days_analyzed > 0 else 0
        
        # Add buffer for variability (50% buffer)
        suggested_daily = daily_average * 1.5
        
        # Calculate suggested balance for target period
        suggested_balance = suggested_daily * target_days
        
        # Ensure minimum balance
        min_balance = 50.0  # Minimum $50
        suggested_balance = max(suggested_balance, min_balance)
        
        # Cap at reasonable maximum
        max_balance = 1000.0  # Maximum $1000 suggestion
        suggested_balance = min(suggested_balance, max_balance)
        
        return Money.from_float(suggested_balance, wallet.currency)
    
    def detect_unusual_activity(
        self,
        wallet: Wallet,
        transactions: List[Transaction],
        lookback_days: int = 7
    ) -> List[str]:
        """
        Detect unusual activity patterns in wallet.
        
        Args:
            wallet: Wallet to analyze
            transactions: Recent transactions
            lookback_days: Days to look back for analysis
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
        recent_transactions = [
            t for t in transactions
            if t.created_at >= cutoff_date and not t.is_reversed
        ]
        
        # Check for rapid consecutive transactions
        if len(recent_transactions) > 10:
            anomalies.append("High transaction frequency detected")
        
        # Check for unusually large transactions
        if recent_transactions:
            amounts = [t.amount.to_float() for t in recent_transactions]
            avg_amount = sum(amounts) / len(amounts)
            max_amount = max(amounts)
            
            if max_amount > avg_amount * 5:  # 5x average
                anomalies.append("Unusually large transaction detected")
        
        # Check for rapid balance changes
        debits = [t for t in recent_transactions if t.is_debit()]
        if len(debits) > 5:
            total_debited = sum(t.amount.to_float() for t in debits)
            if total_debited > wallet.balance.to_float() * 2:
                anomalies.append("High spending rate detected")
        
        # Check for multiple failed transactions (would need access to failed transactions)
        # This would require additional data not available in successful transactions list
        
        return anomalies
    
    def calculate_wallet_health_score(
        self,
        wallet: Wallet,
        transactions: List[Transaction]
    ) -> dict:
        """
        Calculate a health score for the wallet.
        
        Args:
            wallet: Wallet to evaluate
            transactions: Transaction history
            
        Returns:
            Dictionary with health score and factors
        """
        score = 100  # Start with perfect score
        factors = []
        
        # Check balance adequacy
        if wallet.balance.is_zero():
            score -= 30
            factors.append("Zero balance")
        elif wallet.balance.to_float() < 10.0:
            score -= 15
            factors.append("Low balance")
        
        # Check transaction activity
        recent_transactions = [
            t for t in transactions
            if t.created_at >= datetime.utcnow() - timedelta(days=30)
        ]
        
        if not recent_transactions:
            score -= 10
            factors.append("No recent activity")
        elif len(recent_transactions) > 50:
            score -= 5
            factors.append("Very high activity")
        
        # Check for wallet status
        if wallet.status.value != "active":
            score -= 40
            factors.append(f"Wallet status: {wallet.status.value}")
        
        # Check for unusual patterns
        anomalies = self.detect_unusual_activity(wallet, transactions)
        if anomalies:
            score -= len(anomalies) * 5
            factors.extend(anomalies)
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        # Determine health level
        if score >= 90:
            health_level = "Excellent"
        elif score >= 75:
            health_level = "Good"
        elif score >= 60:
            health_level = "Fair"
        elif score >= 40:
            health_level = "Poor"
        else:
            health_level = "Critical"
        
        return {
            "score": score,
            "health_level": health_level,
            "factors": factors,
            "recommendations": self._generate_recommendations(wallet, factors)
        }
    
    def _generate_recommendations(
        self,
        wallet: Wallet,
        factors: List[str]
    ) -> List[str]:
        """Generate recommendations based on wallet factors."""
        recommendations = []
        
        if "Zero balance" in factors:
            recommendations.append("Add funds to your wallet for seamless transactions")
        
        if "Low balance" in factors:
            recommendations.append("Consider adding more funds to avoid payment delays")
        
        if "No recent activity" in factors:
            recommendations.append("Wallet appears inactive - consider using it for payments")
        
        if "Very high activity" in factors:
            recommendations.append("Monitor your spending patterns for budget management")
        
        if any("Unusual" in factor for factor in factors):
            recommendations.append("Review recent transactions for any unauthorized activity")
        
        if not recommendations:
            recommendations.append("Wallet is in good health - continue current usage patterns")
        
        return recommendations
