# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Payment Entity (Domain Layer)

- **ID**: "payment-entity"
- **Title**: "Payment Entity (Domain Layer)"
- **Description**: "Core Payment aggregate root with domain events, business rules, and state transitions."
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Clean Architecture
  - Domain-Driven Design
  - Aggregate Pattern

#### Files (`CodeFile[]`)

- **Name**: "payment.py"
- **Path**: "app/payments/domain/entities/payment.py"
- **Language**: "python"
- **Content**:
  ```python
  class Payment(AggregateRoot):
      id: PaymentId
      user_id: UserId
      amount: Money
      payment_method: PaymentMethod
      payment_type: PaymentType
      status: PaymentStatus

      @classmethod
      def create(cls, user_id, amount, payment_method, payment_type, metadata=None):
          if amount.amount <= 0:
              raise InvalidPaymentAmountException(amount.to_float())
          
          payment = cls(
              id=PaymentId.generate(),
              user_id=user_id,
              amount=amount,
              payment_method=payment_method,
              payment_type=payment_type,
              status=PaymentStatus.PENDING,
              # ...
          )
          payment._add_event(PaymentCreated(...))
          return payment

      def complete(self, transaction_reference=None):
          if not self.can_be_completed():
              raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
          self.status = PaymentStatus.COMPLETED
          self.completed_at = datetime.now(timezone.utc)
          self._add_event(PaymentCompleted(...))
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Payment entity is an aggregate root that encapsulates all business logic for payment processing, including state transitions, refund handling, and event emission."

---

### Example 2: Kafka Event Publishing

- **ID**: "kafka-publisher"
- **Title**: "Kafka Event Publishing"
- **Description**: "Infrastructure adapter for publishing payment events to Kafka."
- **Category**: "Infrastructure"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Kafka
  - Event-Driven
  - Infrastructure

#### Files (`CodeFile[]`)

- **Name**: "kafka_payment_events.py"
- **Path**: "app/payments/infrastructure/messaging/kafka_payment_events.py"
- **Language**: "python"
- **Content**:
  ```python
  class KafkaPaymentEventsPublisher(PaymentEventsPublisher):
      def __init__(self, producer: KafkaProducer, topic: str) -> None:
          self._producer = producer
          self._topic = topic

      async def publish(self, event_name, payload, key=None):
          message = {
              "event_type": event_name,
              "service": settings.SERVICE_NAME,
              "payload": payload,
          }
          value = json.dumps(message, default=str).encode("utf-8")
          kafka_key = key.encode("utf-8") if key else None
          self._producer.send(topic=self._topic, key=kafka_key, value=value)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The KafkaPaymentEventsPublisher is an adapter that implements the PaymentEventsPublisher interface, enabling event-driven communication with other microservices."

---

### Example 3: Customer Payment Controller

- **ID**: "customer-controller"
- **Title**: "Customer Payment Controller"
- **Description**: "FastAPI controller with JWT authentication and dependency injection."
- **Category**: "Presentation"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - FastAPI
  - REST API
  - Dependency Injection

#### Files (`CodeFile[]`)

- **Name**: "customer_payment_controller.py"
- **Path**: "app/payments/presentation/controllers/customer_payment_controller.py"
- **Language**: "python"
- **Content**:
  ```python
  @router.post("/tickets", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
  async def purchase_tickets(
      body: TicketPurchaseRequest,
      user: AuthUserContext = Depends(get_current_user),
      use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
  ) -> PaymentResponse:
      payment = await use_case.purchase_tickets(body.to_command(str(user.id)))
      return PaymentResponse.from_entity(payment)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The controller demonstrates Clean Architecture at the presentation layer with FastAPI dependency injection for use cases and automatic JWT authentication."

---

### Example 4: Money Value Object

- **ID**: "money-value-object"
- **Title**: "Money Value Object"
- **Description**: "Immutable value object for type-safe monetary operations."
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Value Object
  - Immutability
  - Type Safety

#### Files (`CodeFile[]`)

- **Name**: "value_objects.py"
- **Path**: "app/payments/domain/value_objects.py"
- **Language**: "python"
- **Content**:
  ```python
  class Money(BaseModel):
      model_config = ConfigDict(frozen=True)
      amount: Decimal
      currency: Currency

      def add(self, other: Money) -> Money:
          if self.currency != other.currency:
              raise ValueError(f"Cannot add {self.currency} and {other.currency}")
          return Money(amount=self.amount + other.amount, currency=self.currency)

      def subtract(self, other: Money) -> Money:
          if self.currency != other.currency:
              raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
          return Money(amount=self.amount - other.amount, currency=self.currency)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Money value object ensures type safety for all monetary operations with currency validation and immutable semantics."

---

### Example 5: JWT Authentication

- **ID**: "jwt-auth"
- **Title**: "JWT Authentication & RBAC"
- **Description**: "Role-based access control with JWT token validation."
- **Category**: "Security"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - JWT
  - RBAC
  - Security

#### Files (`CodeFile[]`)

- **Name**: "auth.py"
- **Path**: "app/shared/auth.py"
- **Language**: "python"
- **Content**:
  ```python
  ADMIN_ROLE_NAMES = frozenset({"admin", "superadmin"})

  async def require_admin_user(user: AuthUserContext = Depends(get_current_user)):
      if not is_admin_user(user):
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="This action requires an admin role.",
          )
      return user

  def is_admin_user(user: AuthUserContext) -> bool:
      return any(r.strip().lower() in ADMIN_ROLE_NAMES for r in user.roles)
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "JWT authentication with role-based access control ensures proper authorization for admin, staff, and customer endpoints."

---

### Example 6: Domain Events

- **ID**: "domain-events"
- **Title**: "Domain Events"
- **Description**: "Domain events for payment lifecycle tracking."
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Domain Events
  - Event-Driven
  - Audit Trail

#### Files (`CodeFile[]`)

- **Name**: "events.py"
- **Path**: "app/payments/domain/events.py"
- **Language**: "python"
- **Content**:
  ```python
  class PaymentCompleted(DomainEvent):
      payment_id: PaymentId
      user_id: UserId
      amount: Money
      payment_type: PaymentType
      transaction_reference: Optional[str] = None

      def event_type(self) -> str:
          return "payment.completed"

      def _get_event_data(self) -> Dict[str, Any]:
          return {
              "payment_id": str(self.payment_id),
              "amount": self.amount.to_float(),
              "currency": self.amount.currency.value,
              # ...
          }
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Domain events capture significant business occurrences and provide an audit trail for the payment lifecycle."
