"""
Payment Application Service

Orchestrates payment operations using CQRS pattern with command and query handlers.
This service acts as the application facade and coordinates business workflows.
"""

from typing import Union, Dict, Any
from uuid import UUID

from app.application.commands.procces_pay.procces_pay import (
    ProcessPayCommand, ProcessPaymentCommandHandler, ProcessPaymentResult
)
from app.application.commands.refund_pay.refund_pay import (
    RefundPaymentCommand, RefundPaymentCommandHandler, RefundPaymentResult
)
from app.application.commands.credit.add_credit import (
    AddCreditCommand, AddCreditCommandHandler, AddCreditResult
)
from app.application.queries.get_history import (
    GetPaymentHistoryQuery, GetPaymentHistoryQueryHandler, PaymentHistoryResult
)
from app.application.queries.get_transaction import (
    GetTransactionQuery, GetTransactionQueryHandler, GetTransactionResult
)
from app.application.interfaces import (
    EventPublisher, PaymentGateway, NotificationService, 
    WalletRepository, TransactionRepository
)
from app.domain.repository.payment_repository import PaymentRepository


class PaymentApplicationService:
    """
    Application service for payment operations.
    
    Provides a unified interface for all payment-related commands and queries,
    implementing the CQRS pattern with proper separation of concerns.
    """
    
    def __init__(
        self,
        payment_repository: PaymentRepository,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
        event_publisher: EventPublisher,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService
    ):
        self.payment_repository = payment_repository
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository
        self.event_publisher = event_publisher
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
        
        # Initialize command handlers
        self._process_payment_handler = ProcessPaymentCommandHandler(
            payment_repository=payment_repository,
            wallet_repository=wallet_repository,
            event_publisher=event_publisher,
            payment_gateway=payment_gateway,
            notification_service=notification_service
        )
        
        self._refund_payment_handler = RefundPaymentCommandHandler(
            payment_repository=payment_repository,
            wallet_repository=wallet_repository,
            event_publisher=event_publisher,
            payment_gateway=payment_gateway,
            notification_service=notification_service
        )
        
        self._add_credit_handler = AddCreditCommandHandler(
            wallet_repository=wallet_repository,
            event_publisher=event_publisher,
            notification_service=notification_service
        )
        
        # Initialize query handlers
        self._get_payment_history_handler = GetPaymentHistoryQueryHandler(
            payment_repository=payment_repository
        )
        
        self._get_transaction_handler = GetTransactionQueryHandler(
            payment_repository=payment_repository,
            transaction_repository=transaction_repository,
            wallet_repository=wallet_repository
        )
    
    # Command Operations
    
    async def process_payment(self, command: ProcessPayCommand) -> ProcessPaymentResult:
        """
        Process a payment transaction.
        
        Args:
            command: Payment processing command
            
        Returns:
            Payment processing result
        """
        return await self._process_payment_handler.handle(command)
    
    async def refund_payment(self, command: RefundPaymentCommand) -> RefundPaymentResult:
        """
        Process a payment refund.
        
        Args:
            command: Payment refund command
            
        Returns:
            Payment refund result
        """
        return await self._refund_payment_handler.handle(command)
    
    async def add_credit(self, command: AddCreditCommand) -> AddCreditResult:
        """
        Add credit to a user's wallet.
        
        Args:
            command: Add credit command
            
        Returns:
            Add credit result
        """
        return await self._add_credit_handler.handle(command)
    
    # Query Operations
    
    async def get_payment_history(self, query: GetPaymentHistoryQuery) -> PaymentHistoryResult:
        """
        Get payment history for a user.
        
        Args:
            query: Payment history query
            
        Returns:
            Payment history result
        """
        return await self._get_payment_history_handler.handle(query)
    
    async def get_transaction_details(self, query: GetTransactionQuery) -> GetTransactionResult:
        """
        Get detailed transaction information.
        
        Args:
            query: Transaction details query
            
        Returns:
            Transaction details result
        """
        return await self._get_transaction_handler.handle(query)
    
    # Convenience Methods
    
    async def process_ticket_payment(
        self,
        user_id: UUID,
        amount: float,
        payment_method: str,
        ticket_ids: list[str],
        showtime_id: str,
        seat_numbers: list[str],
        currency: str = "USD"
    ) -> ProcessPaymentResult:
        """
        Convenience method for processing ticket payments.
        
        Args:
            user_id: User making the payment
            amount: Payment amount
            payment_method: Payment method
            ticket_ids: List of ticket IDs
            showtime_id: Showtime identifier
            seat_numbers: List of seat numbers
            currency: Payment currency
            
        Returns:
            Payment processing result
        """
        command = ProcessPayCommand(
            product_id=UUID(int=0),  # Could be derived from showtime_id
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            payment_type="ticket_purchase",
            currency=currency,
            metadata={
                "ticket_ids": ticket_ids,
                "showtime_id": showtime_id,
                "seat_numbers": seat_numbers
            }
        )
        
        return await self.process_payment(command)
    
    async def process_food_payment(
        self,
        user_id: UUID,
        amount: float,
        payment_method: str,
        food_items: list[dict],
        pickup_location: str,
        currency: str = "USD"
    ) -> ProcessPaymentResult:
        """
        Convenience method for processing food payments.
        
        Args:
            user_id: User making the payment
            amount: Payment amount
            payment_method: Payment method
            food_items: List of food items
            pickup_location: Pickup location
            currency: Payment currency
            
        Returns:
            Payment processing result
        """
        command = ProcessPayCommand(
            product_id=UUID(int=0),  # Could be derived from food items
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            payment_type="food_purchase",
            currency=currency,
            metadata={
                "food_items": food_items,
                "pickup_location": pickup_location
            }
        )
        
        return await self.process_payment(command)
    
    async def top_up_wallet(
        self,
        user_id: UUID,
        amount: float,
        reference_id: str,
        description: str = "Wallet top-up",
        currency: str = "USD"
    ) -> AddCreditResult:
        """
        Convenience method for wallet top-up.
        
        Args:
            user_id: User whose wallet to credit
            amount: Amount to add
            reference_id: External reference
            description: Description of the credit
            currency: Currency
            
        Returns:
            Add credit result
        """
        command = AddCreditCommand(
            user_id=user_id,
            amount=amount,
            currency=currency,
            reference_id=reference_id,
            source="payment",
            description=description
        )
        
        return await self.add_credit(command)
    
    async def get_user_payment_history(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> PaymentHistoryResult:
        """
        Convenience method to get user's payment history.
        
        Args:
            user_id: User ID
            limit: Maximum records to return
            offset: Number of records to skip
            
        Returns:
            Payment history result
        """
        query = GetPaymentHistoryQuery(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        return await self.get_payment_history(query)
    
    async def get_payment_by_id(self, payment_id: UUID) -> GetTransactionResult:
        """
        Convenience method to get payment details by ID.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Transaction result with payment details
        """
        query = GetTransactionQuery(
            payment_id=payment_id,
            include_payment_details=True,
            include_wallet_details=True
        )
        
        return await self.get_transaction_details(query)
    
    async def get_wallet_transactions(
        self,
        user_id: UUID,
        include_wallet_details: bool = True
    ) -> GetTransactionResult:
        """
        Convenience method to get wallet transactions for a user.
        
        Args:
            user_id: User ID
            include_wallet_details: Whether to include wallet details
            
        Returns:
            Transaction result with wallet transactions
        """
        query = GetTransactionQuery(
            user_id=user_id,
            include_wallet_details=include_wallet_details
        )
        
        return await self.get_transaction_details(query)


class CommandBus:
    """Simple command bus for routing commands to appropriate handlers."""
    
    def __init__(self, payment_service: PaymentApplicationService):
        self.payment_service = payment_service
        self._handlers = {
            ProcessPayCommand: payment_service.process_payment,
            RefundPaymentCommand: payment_service.refund_payment,
            AddCreditCommand: payment_service.add_credit,
        }
    
    async def execute(self, command) -> Union[ProcessPaymentResult, RefundPaymentResult, AddCreditResult]:
        """Execute a command using the appropriate handler."""
        command_type = type(command)
        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for command type {command_type}")
        
        handler = self._handlers[command_type]
        return await handler(command)


class QueryBus:
    """Simple query bus for routing queries to appropriate handlers."""
    
    def __init__(self, payment_service: PaymentApplicationService):
        self.payment_service = payment_service
        self._handlers = {
            GetPaymentHistoryQuery: payment_service.get_payment_history,
            GetTransactionQuery: payment_service.get_transaction_details,
        }
    
    async def execute(self, query) -> Union[PaymentHistoryResult, GetTransactionResult]:
        """Execute a query using the appropriate handler."""
        query_type = type(query)
        if query_type not in self._handlers:
            raise ValueError(f"No handler registered for query type {query_type}")
        
        handler = self._handlers[query_type]
        return await handler(query)
