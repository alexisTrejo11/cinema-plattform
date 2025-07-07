# Payment Service Domain Layer

This document provides an overview of the domain layer architecture following Domain-Driven Design (DDD) principles and Clean Architecture patterns.





## 🏗️ Domain Architecture Overview

```
app/domain/
├── __init__.py                 # Domain package
├── exceptions.py               # Domain-specific exceptions
├── value_objects.py           # Immutable value objects
├── events.py                  # Domain events for event sourcing
├── entities/                  # Domain entities (aggregates)
│   ├── __init__.py
│   ├── payment.py            # Payment aggregate root
│   ├── wallet.py             # Wallet aggregate root
│   └── transaction.py        # Transaction entity
└── services/                  # Domain services
    ├── __init__.py
    ├── payment_service.py    # Payment business logic
    └── wallet_service.py     # Wallet business logic
```





## 🎯 Core Domain Concepts

### Value Objects

**Immutable objects representing domain concepts without identity:**

- **Money**: Monetary amounts with currency and proper arithmetic
- **PaymentId, WalletId, TransactionId**: Typed identifiers
- **PaymentStatus, PaymentType, PaymentMethod**: Enumerations
- **PaymentReference**: External payment gateway references
- **PaymentMetadata**: Contextual payment information

### Entities (Aggregates)

**Business objects with identity and lifecycle:**

#### Payment Aggregate
- **Purpose**: Core payment processing with business rules
- **Responsibilities**:
  - Payment lifecycle management (pending → processing → completed/failed)
  - Refund processing with business rules
  - Payment expiry and validation
  - Domain event generation
- **Key Methods**:
  - `create()`: Factory method with business validation
  - `start_processing()`: Begin payment processing
  - `complete()`: Mark payment as successful
  - `fail()`: Handle payment failures
  - `refund()`: Process refunds with business rules
  - `can_be_*()`: Business rule validation

#### Wallet Aggregate
- **Purpose**: User credit management with transaction history
- **Responsibilities**:
  - Balance management with currency consistency
  - Credit/debit operations with validation
  - Transaction limits and controls
  - Wallet status management
  - Domain event generation
- **Key Methods**:
  - `create()`: Factory method for new wallets
  - `credit()`: Add funds with validation
  - `debit()`: Remove funds with insufficient funds checking
  - `can_debit()`: Balance validation
  - `suspend()`, `activate()`: Status management

#### Transaction Entity
- **Purpose**: Immutable transaction records for audit trail
- **Responsibilities**:
  - Transaction history tracking
  - Balance before/after tracking
  - Transaction reversal support
  - Audit trail maintenance

### Domain Services

**Services handling complex business logic spanning multiple aggregates:**

#### PaymentDomainService
- **Purpose**: Complex payment operations and calculations
- **Capabilities**:
  - Payment fee calculations based on method and type
  - Bulk discount calculations
  - Refund amount calculations with policies
  - Payment method suggestions
  - Fraud detection patterns
  - Payment expiry calculations

#### WalletDomainService
- **Purpose**: Multi-wallet operations and analytics
- **Capabilities**:
  - Wallet-to-wallet transfers with fees
  - Wallet health scoring and metrics
  - Optimal balance suggestions
  - Unusual activity detection
  - Daily limit validations

### Domain Events

**Events representing significant business occurrences:**

#### Payment Events
- `PaymentCreated`: New payment initiated
- `PaymentProcessingStarted`: Payment processing began
- `PaymentCompleted`: Payment successfully processed
- `PaymentFailed`: Payment processing failed
- `PaymentRefunded`: Payment refunded

#### Wallet Events
- `WalletCredited`: Funds added to wallet
- `WalletDebited`: Funds removed from wallet
- `InsufficientFundsDetected`: Attempted transaction with insufficient funds
- `TransactionRecorded`: New transaction recorded

### Domain Exceptions

**Business rule violations and error conditions:**

- `PaymentAlreadyProcessedException`: Payment state violations
- `PaymentNotRefundableException`: Refund policy violations
- `InsufficientFundsException`: Wallet balance violations
- `InvalidPaymentAmountException`: Amount validation failures
- `WalletNotActiveException`: Wallet status violations

## 🔒 Business Rules Implementation

### Payment Rules

1. **Amount Validation**:
   - Minimum payment amount enforcement
   - Maximum payment limits by type
   - Currency consistency checks

2. **Status Transitions**:
   - Only pending payments can be processed
   - Only processing payments can be completed
   - Only completed payments can be refunded

3. **Refund Policies**:
   - Time-based refund percentages for tickets
   - Partial refund fees
   - Maximum refundable amount tracking

4. **Expiry Management**:
   - Payment-specific expiry times
   - Method-based expiry adjustments

### Wallet Rules

1. **Balance Management**:
   - Non-negative balance enforcement
   - Currency consistency validation
   - Minimum balance requirements

2. **Transaction Limits**:
   - Daily transaction limits
   - Monthly transaction limits
   - Maximum balance limits

3. **Status Controls**:
   - Only active wallets allow transactions
   - Suspended wallets block operations
   - Closed wallets require zero balance

### Transfer Rules

1. **Multi-Wallet Operations**:
   - Currency compatibility checks
   - Fee calculations with min/max limits
   - Sufficient funds validation

2. **Security Controls**:
   - Daily transfer limits
   - Unusual activity detection
   - Transaction pattern analysis



## 🎭 Domain Events Flow

```
Payment Creation:
PaymentCreated → [External Systems Notified]

Payment Processing:
PaymentProcessingStarted → [Gateway Integration] → PaymentCompleted/PaymentFailed

Wallet Operations:
WalletDebited → TransactionRecorded → [Balance Updated]
WalletCredited → TransactionRecorded → [Balance Updated]

Refund Processing:
PaymentRefunded → WalletCredited → [User Notified]
```


## 💡 Design Patterns Used

### Aggregate Pattern
- Clear aggregate boundaries with Payment and Wallet as roots
- Consistency boundaries maintained within aggregates
- External access only through aggregate roots

### Value Object Pattern
- Immutable objects for Money, IDs, and descriptive data
- Proper encapsulation of validation logic
- Type safety through strong typing

### Domain Service Pattern
- Complex business logic extracted from entities
- Coordination between multiple aggregates
- Stateless operations with clear interfaces

### Domain Event Pattern
- Loose coupling between bounded contexts
- Event-driven architecture support
- Audit trail and integration capabilities

### Factory Pattern
- Controlled object creation with validation
- Business rule enforcement at creation time
- Consistent initialization across aggregates







## 🧪 Business Logic Examples

### Payment Processing Flow
```python
# Create a new payment
payment = Payment.create(
    user_id=UserId.from_string("user-123"),
    amount=Money.from_float(29.99, Currency.USD),
    payment_method=PaymentMethod.STRIPE,
    payment_type=PaymentType.TICKET_PURCHASE,
    metadata=PaymentMetadata(ticket_ids=["ticket-1", "ticket-2"])
)

# Start processing
payment.start_processing(
    external_reference=PaymentReference("stripe", "pi_1234567890")
)

# Complete payment
payment.complete("ch_1234567890")

# Events generated:
# - PaymentCreated
# - PaymentProcessingStarted  
# - PaymentCompleted
```

### Wallet Operations
```python
# Create wallet
wallet = Wallet.create(
    user_id=UserId.from_string("user-123"),
    currency=Currency.USD
)

# Add funds
transaction_id = wallet.credit(
    amount=Money.from_float(100.00, Currency.USD),
    description="Credit card top-up",
    reference_id="payment-123"
)

# Make payment
if wallet.can_debit(Money.from_float(29.99, Currency.USD)):
    wallet.debit(
        amount=Money.from_float(29.99, Currency.USD),
        description="Ticket purchase",
        reference_id="payment-456"
    )

# Events generated:
# - WalletCredited + TransactionRecorded
# - WalletDebited + TransactionRecorded
```

### Complex Business Logic
```python
# Using domain services
payment_service = PaymentDomainService()

# Calculate fees
fees = payment_service.calculate_payment_fees(
    amount=Money.from_float(100.00, Currency.USD),
    payment_method=PaymentMethod.CREDIT_CARD,
    payment_type=PaymentType.TICKET_PURCHASE
)

# Calculate refund amount with policies
refund_amount = payment_service.calculate_refund_amount(
    payment=completed_payment,
    refund_percentage=Decimal('0.95')  # 95% refund
)

# Wallet health analysis
wallet_service = WalletDomainService()
health_score = wallet_service.calculate_wallet_health_score(
    wallet=user_wallet,
    transactions=recent_transactions
)
```





## 🔄 Integration Points

### Event Publishing
- Domain events are collected within aggregates
- Events published after successful persistence
- Supports eventual consistency across services

### External Services
- Payment gateways integrated through domain interfaces
- External references tracked in value objects
- Gateway-specific logic isolated from domain

### Data Persistence
- Aggregates serialized maintaining business invariants
- Event sourcing supported through domain events
- Repository pattern for aggregate persistence

This domain layer provides a robust foundation for the payment service, ensuring business rules are properly encapsulated, maintained, and evolved while supporting complex payment scenarios in a cinema context.
