# Payment Service - Application Layer

The application layer implements the CQRS (Command Query Responsibility Segregation) pattern, providing a clean separation between command operations (write) and query operations (read). This layer orchestrates domain objects and handles business workflows while maintaining proper separation of concerns.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
├─────────────────────┬─────────────────────┬─────────────────┤
│      Commands       │      Queries        │    Services     │
│   (Write Side)      │   (Read Side)       │  (Orchestration)│
├─────────────────────┼─────────────────────┼─────────────────┤
│ • ProcessPayment    │ • GetPaymentHistory │ • PaymentApp    │
│ • RefundPayment     │ • GetTransaction    │   Service       │
│ • AddCredit         │                     │ • CommandBus    │
│                     │                     │ • QueryBus      │
└─────────────────────┴─────────────────────┴─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  • Entities (Payment, Wallet, Transaction)                 │
│  • Value Objects (Money, PaymentId, etc.)                  │
│  • Domain Events                                           │
│  • Business Rules & Invariants                             │
└─────────────────────────────────────────────────────────────┘
```

## Commands (Write Operations)

Commands represent intentions to change the system state. They contain all the data needed to perform an operation and are handled by dedicated command handlers.

### ProcessPaymentCommand

Processes a new payment transaction with support for multiple payment methods.

**Features:**
- Credit card, wallet, PayPal, and Stripe payment processing
- Real-time business rule validation
- Automatic event publishing
- Transaction rollback on failure
- Notification sending

**Usage:**
```python
command = ProcessPayCommand(
    product_id="12345678-1234-1234-1234-123456789012",
    user_id="87654321-4321-4321-4321-210987654321",
    amount=150.75,
    payment_method="wallet",
    payment_type="ticket_purchase",
    currency="USD",
    metadata={
        "ticket_ids": ["ticket_1", "ticket_2"],
        "showtime_id": "show_123",
        "seat_numbers": ["A1", "A2"]
    }
)
result = await payment_service.process_payment(command)
```

### RefundPaymentCommand

Handles payment refunds with flexible refund destinations.

**Features:**
- Full and partial refunds
- Refund to original payment method or wallet
- Business rule validation (refund windows, amounts)
- Automatic wallet crediting for wallet refunds
- Event publishing and notifications

**Usage:**
```python
command = RefundPaymentCommand(
    payment_id="12345678-1234-1234-1234-123456789012",
    refund_amount=75.50,  # Optional, full refund if not specified
    reason="Customer requested refund due to event cancellation",
    requested_by="admin_user_id",
    refund_to_wallet=True
)
result = await payment_service.refund_payment(command)
```

### AddCreditCommand

Adds credit to user wallets with full audit trail.

**Features:**
- Multi-currency support
- Automatic wallet creation if needed
- Currency validation
- Transaction recording
- Event publishing

**Usage:**
```python
command = AddCreditCommand(
    user_id="87654321-4321-4321-4321-210987654321",
    amount=50.00,
    currency="USD",
    reference_id="topup_123456",
    source="payment",
    description="Credit from PayPal top-up"
)
result = await payment_service.add_credit(command)
```

## Queries (Read Operations)

Queries retrieve data without modifying system state. They provide flexible filtering, sorting, and pagination capabilities.

### GetPaymentHistoryQuery

Retrieves paginated payment history with filtering options.

**Features:**
- User-based filtering
- Status and payment type filtering
- Date range filtering
- Flexible sorting and pagination
- Rich payment details

**Usage:**
```python
query = GetPaymentHistoryQuery(
    user_id="87654321-4321-4321-4321-210987654321",
    status="completed",
    payment_type="ticket_purchase",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    limit=25,
    offset=0,
    sort_by="created_at",
    sort_order="desc"
)
result = await payment_service.get_payment_history(query)
```

### GetTransactionQuery

Retrieves detailed transaction information with related data.

**Features:**
- Transaction lookup by multiple identifiers
- Payment and wallet context inclusion
- Related transaction discovery
- Comprehensive transaction details

**Usage:**
```python
# Get by transaction ID
query = GetTransactionQuery(
    transaction_id="12345678-1234-1234-1234-123456789012",
    include_payment_details=True,
    include_wallet_details=True
)

# Get by payment ID
query = GetTransactionQuery(
    payment_id="87654321-4321-4321-4321-210987654321",
    include_wallet_details=True
)

# Get wallet transactions for user
query = GetTransactionQuery(
    user_id="87654321-4321-4321-4321-210987654321",
    include_wallet_details=True
)

result = await payment_service.get_transaction_details(query)
```

## Application Service

The `PaymentApplicationService` acts as the main facade for all payment operations, providing:

### Core Operations
- **process_payment()** - Process new payments
- **refund_payment()** - Handle payment refunds
- **add_credit()** - Add credit to wallets
- **get_payment_history()** - Retrieve payment history
- **get_transaction_details()** - Get transaction information

### Convenience Methods
- **process_ticket_payment()** - Simplified ticket payment processing
- **process_food_payment()** - Simplified food payment processing
- **top_up_wallet()** - Simplified wallet top-up
- **get_user_payment_history()** - User payment history with defaults
- **get_payment_by_id()** - Payment lookup by ID
- **get_wallet_transactions()** - User wallet transactions

### Example Usage
```python
# Initialize the service
payment_service = PaymentApplicationService(
    payment_repository=payment_repo,
    wallet_repository=wallet_repo,
    transaction_repository=transaction_repo,
    event_publisher=event_publisher,
    payment_gateway=payment_gateway,
    notification_service=notification_service
)

# Process a ticket payment
result = await payment_service.process_ticket_payment(
    user_id=user_id,
    amount=45.00,
    payment_method="credit_card",
    ticket_ids=["ticket_123"],
    showtime_id="show_456",
    seat_numbers=["A1"]
)

# Add wallet credit
credit_result = await payment_service.top_up_wallet(
    user_id=user_id,
    amount=100.00,
    reference_id="stripe_payment_123"
)

# Get payment history
history = await payment_service.get_user_payment_history(
    user_id=user_id,
    limit=20
)
```

## Command and Query Buses

The application layer includes simple bus implementations for routing commands and queries to their appropriate handlers.

### CommandBus
Routes commands to the correct handler:
```python
command_bus = CommandBus(payment_service)
result = await command_bus.execute(ProcessPayCommand(...))
```

### QueryBus
Routes queries to the correct handler:
```python
query_bus = QueryBus(payment_service)
result = await query_bus.execute(GetPaymentHistoryQuery(...))
```

## Event Handling

The application layer integrates with the domain events system:

### Event Publishing
- Automatically publishes domain events after successful operations
- Handles event batching for performance
- Ensures events are cleared after publishing

### Event Types Published
- **PaymentCreated** - When a new payment is initiated
- **PaymentProcessingStarted** - When payment processing begins
- **PaymentCompleted** - When payment is successfully processed
- **PaymentFailed** - When payment processing fails
- **PaymentRefunded** - When a refund is processed
- **WalletCredited** - When wallet receives credit
- **WalletDebited** - When wallet is debited
- **TransactionRecorded** - When transactions are created

## Business Logic Integration

The application layer enforces business rules through:

### Validation
- Input validation using Pydantic models
- Business rule validation through domain entities
- Cross-aggregate consistency checks

### Error Handling
- Graceful error handling with meaningful messages
- Automatic rollback of failed operations
- Proper exception propagation

### Transaction Management
- Ensures data consistency across repositories
- Handles concurrent access scenarios
- Manages distributed transaction scenarios

## Dependencies

The application layer depends on:

### Interfaces
- **PaymentRepository** - Payment data access
- **WalletRepository** - Wallet data access  
- **TransactionRepository** - Transaction data access
- **EventPublisher** - Event publishing
- **PaymentGateway** - External payment processing
- **NotificationService** - User notifications

### Domain Layer
- Domain entities and value objects
- Domain events
- Business rules and exceptions

## Testing Strategy

### Unit Testing
- Test each command handler in isolation
- Test each query handler in isolation
- Mock all external dependencies
- Verify domain events are published

### Integration Testing
- Test complete workflows end-to-end
- Test error scenarios and rollbacks
- Test event publishing integration
- Test notification sending

### Example Test
```python
async def test_process_payment_command_handler():
    # Arrange
    handler = ProcessPaymentCommandHandler(...)
    command = ProcessPayCommand(...)
    
    # Act
    result = await handler.handle(command)
    
    # Assert
    assert result.status == "completed"
    assert result.payment_id is not None
    payment_repo.save.assert_called_once()
    event_publisher.publish_batch.assert_called_once()
```

## Performance Considerations

### Scalability
- Handlers are stateless and can be scaled horizontally
- Event publishing is asynchronous to avoid blocking
- Query operations support pagination

### Caching
- Query results can be cached at the infrastructure layer
- Event sourcing enables read model optimization
- Aggregate snapshots can improve performance

### Monitoring
- All operations emit events for monitoring
- Command/query execution times tracked
- Business metrics available through events

## Configuration

The application layer requires configuration for:

### Repository Implementations
```python
payment_repository = SqlAlchemyPaymentRepository(...)
wallet_repository = SqlAlchemyWalletRepository(...)
transaction_repository = SqlAlchemyTransactionRepository(...)
```

### External Services
```python
event_publisher = RabbitMQEventPublisher(...)
payment_gateway = StripePaymentGateway(...)
notification_service = EmailNotificationService(...)
```

### Service Initialization
```python
payment_service = PaymentApplicationService(
    payment_repository=payment_repository,
    wallet_repository=wallet_repository,
    transaction_repository=transaction_repository,
    event_publisher=event_publisher,
    payment_gateway=payment_gateway,
    notification_service=notification_service
)
```

This application layer provides a robust, scalable foundation for payment processing with clear separation of concerns, comprehensive error handling, and full business rule enforcement.
