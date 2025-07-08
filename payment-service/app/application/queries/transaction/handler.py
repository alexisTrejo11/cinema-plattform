from app.domain.value_objects import PaymentId, TransactionId, WalletId, UserId
from app.domain.repository.payment_repository import PaymentRepository
from app.application.interfaces import TransactionRepository, WalletRepository
from .query import GetTransactionQuery
from .result import GetTransactionResult, WalletDetail, PaymentDetail, TransactionDetail

class GetTransactionQueryHandler:
    """Handler for getting transaction details."""
    def __init__(
        self,
        payment_repository: PaymentRepository,
        transaction_repository: TransactionRepository,
        wallet_repository: WalletRepository
    ):
        self.payment_repository = payment_repository
        self.transaction_repository = transaction_repository
        self.wallet_repository = wallet_repository
    
    async def handle(self, query: GetTransactionQuery) -> GetTransactionResult:
        """
        Handle transaction query.
        
        Args:
            query: Transaction query
            
        Returns:
            Transaction query result
        """
        try:
            result = GetTransactionResult()
            
            # Handle different query types
            if query.transaction_id:
                result = await self._get_by_transaction_id(query, result)
            elif query.payment_id:
                result = await self._get_by_payment_id(query, result)
            elif query.wallet_id or query.user_id:
                result = await self._get_by_wallet_or_user(query, result)
            else:
                result.message = "No valid identifier provided"
                return result
            
            return result
            
        except Exception as e:
            return GetTransactionResult(
                found=False,
                message=f"Error retrieving transaction: {str(e)}"
            )
    
    async def _get_by_transaction_id(
        self, 
        query: GetTransactionQuery, 
        result: GetTransactionResult
    ) -> GetTransactionResult:
        """Get transaction by transaction ID."""
        transaction_id = TransactionId.from_string(str(query.transaction_id))
        transaction = await self.transaction_repository.get_by_id(transaction_id)
        
        if not transaction:
            result.message = f"Transaction {query.transaction_id} not found"
            return result
        
        result.transaction = await self._convert_transaction_to_detail(transaction)
        result.found = True
        
        # Include wallet details if requested
        if query.include_wallet_details:
            wallet = await self.wallet_repository.get_by_id(transaction.wallet_id)
            if wallet:
                result.wallet = await self._convert_wallet_to_detail(wallet)
        
        # Include payment details if requested and available
        if query.include_payment_details and transaction.reference_id:
            try:
                payment_id = PaymentId.from_string(transaction.reference_id)
                payment = await self.payment_repository.get_by_id(payment_id)
                if payment:
                    result.payment = await self._convert_payment_to_detail(payment)
            except:
                pass  # Reference ID might not be a payment ID
        
        # Get related transactions if any
        if transaction.related_transaction_id:
            related = await self.transaction_repository.get_by_id(
                transaction.related_transaction_id
            )
            if related:
                result.related_transactions = [
                    await self._convert_transaction_to_detail(related)
                ]
        
        return result
    
    async def _get_by_payment_id(
        self, 
        query: GetTransactionQuery, 
        result: GetTransactionResult
    ) -> GetTransactionResult:
        """Get transaction by payment ID."""
        payment_id = PaymentId.from_string(str(query.payment_id))
        payment = await self.payment_repository.get_by_id(payment_id)
        
        if not payment:
            result.message = f"Payment {query.payment_id} not found"
            return result
        
        result.payment = await self._convert_payment_to_detail(payment)
        result.found = True
        
        # Try to find related wallet transactions
        if payment.payment_method.value == 'wallet':
            wallet = await self.wallet_repository.get_by_user_id(payment.user_id)
            if wallet:
                # Get transactions related to this payment
                transactions = await self.transaction_repository.get_by_wallet_id(
                    wallet.id, limit=10
                )
                
                # Filter transactions that reference this payment
                related_transactions = [
                    t for t in transactions 
                    if t.reference_id == str(payment.id)
                ]
                
                if related_transactions:
                    result.related_transactions = [
                        await self._convert_transaction_to_detail(t)
                        for t in related_transactions
                    ]
                
                if query.include_wallet_details:
                    result.wallet = await self._convert_wallet_to_detail(wallet)
        
        return result
    
    async def _get_by_wallet_or_user(
        self, 
        query: GetTransactionQuery, 
        result: GetTransactionResult
    ) -> GetTransactionResult:
        """Get transactions by wallet ID or user ID."""
        wallet = None
        
        if query.wallet_id:
            wallet_id = WalletId.from_string(str(query.wallet_id))
            wallet = await self.wallet_repository.get_by_id(wallet_id)
        elif query.user_id:
            user_id = UserId.from_string(str(query.user_id))
            wallet = await self.wallet_repository.get_by_user_id(user_id)
        
        if not wallet:
            result.message = "Wallet not found"
            return result
        
        # Get recent transactions for the wallet
        transactions = await self.transaction_repository.get_by_wallet_id(
            wallet.id, limit=10
        )
        
        if transactions:
            result.related_transactions = [
                await self._convert_transaction_to_detail(t)
                for t in transactions
            ]
            result.found = True
        
        if query.include_wallet_details:
            result.wallet = await self._convert_wallet_to_detail(wallet)
        
        return result
    
    async def _convert_transaction_to_detail(self, transaction) -> TransactionDetail:
        """Convert transaction entity to detail model."""
        return TransactionDetail(
            transaction_id=transaction.id.value,
            wallet_id=transaction.wallet_id.value,
            user_id=transaction.user_id.value,
            amount=transaction.amount.to_float(),
            currency=transaction.amount.currency.value,
            transaction_type=transaction.transaction_type.value,
            description=transaction.description,
            created_at=transaction.created_at,
            processed_at=transaction.processed_at,
            reference_id=transaction.reference_id,
            related_transaction_id=(
                transaction.related_transaction_id.value 
                if transaction.related_transaction_id else None
            ),
            balance_before=(
                transaction.balance_before.to_float() 
                if transaction.balance_before else None
            ),
            balance_after=(
                transaction.balance_after.to_float() 
                if transaction.balance_after else None
            ),
            is_reversed=transaction.is_reversed,
            reversal_reason=transaction.reversal_reason,
            reversed_at=transaction.reversed_at
        )
    
    async def _convert_payment_to_detail(self, payment) -> PaymentDetail:
        """Convert payment entity to detail model."""
        return PaymentDetail(
            payment_id=payment.id.value,
            user_id=payment.user_id.value,
            amount=payment.amount.to_float(),
            currency=payment.amount.currency.value,
            payment_method=payment.payment_method.value,
            payment_type=payment.payment_type.value,
            status=payment.status.value,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            completed_at=payment.completed_at,
            failure_reason=payment.failure_reason,
            metadata=payment.metadata.__dict__ if payment.metadata else None
        )
    
    async def _convert_wallet_to_detail(self, wallet) -> WalletDetail:
        """Convert wallet entity to detail model."""
        return WalletDetail(
            wallet_id=wallet.id.value,
            user_id=wallet.user_id.value,
            current_balance=wallet.balance.to_float(),
            currency=wallet.currency.value,
            status=wallet.status.value,
            created_at=wallet.created_at,
            updated_at=wallet.updated_at,
            last_transaction_at=wallet.last_transaction_at
        )