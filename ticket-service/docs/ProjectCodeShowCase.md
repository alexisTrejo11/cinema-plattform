# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Ticket Purchase Flow (`CodeExample`)

- **ID**: "ticket-purchase-flow"
- **Title**: "Digital Ticket Purchase Use Case"
- **Description**: "Complete ticket purchase workflow showing orchestration of seat validation, payment authorization, and ticket creation"
- **Category**: "Use Case"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `ticket`
  - `purchase`
  - `use-case`

#### Files (`CodeFile[]`)

- **Name**: "ticket_command_use_cases.py"
- **Path**: "app/ticket/application/usecases/ticket_command_use_cases.py"
- **Language**: "python"
- **Content**:
  ```python
  class DigitalBuyTicketsUseCase:
      """
      Orchestrator for the digital purchase flow across services and local data:
      1. Load showtime + seat rows from the local replica (Mongo/Postgres).
      2. Validate seat list locally (existence + availability flags).
      3. Call billboard (gRPC) for source-of-truth concurrency check.
      4. Call payment (gRPC) to authorize funds before mutating inventory.
      5. Take seats, persist ticket, build confirmation (QR, etc.).
      """

      async def execute(self, buy_dto: BuyTicketsRequest) -> TicketPurchasedDetails:
          # Load showtime and seat data
          showtime, showtime_seats = await self._get_showtime_data(buy_dto)
          self._validate_local_seats(buy_dto, showtime_seats)

          # gRPC seat assertion
          if self.seat_assertion:
              await self.seat_assertion.assert_seats_available_for_purchase(
                  buy_dto.showtime_id, list(buy_dto.seat_list_id)
              )

          # gRPC payment authorization
          if self.payment_gateway:
              total = showtime.get_price() * len(buy_dto.seat_list_id)
              auth = await self.payment_gateway.authorize_payment(
                  PaymentAuthorizationRequest(
                      amount=total,
                      currency="MXN",
                      customer_id=buy_dto.customer_id,
                      idempotency_key=f"{buy_dto.customer_id}:{buy_dto.showtime_id}:...",
                      payment_method=buy_dto.payment_method,
                      payment_token=buy_dto.payment_details,
                      customer_ip=buy_dto.customer_ip,
                  )
              )
              if not auth.authorized:
                  raise PaymentAuthorizationFailedError("payment not authorized")

          # Process ticket
          ticket_created = await self._process_ticket(buy_dto, showtime, showtime_seats)
          return await self._generate_ticket_response(ticket_created, showtime)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "This use case demonstrates the orchestration pattern, coordinating multiple services (local repositories, gRPC clients) to complete a ticket purchase with proper validation and error handling."

---

### Example 2: Ticket Entity (`CodeExample`)

- **ID**: "ticket-entity"
- **Title**: "Ticket Domain Entity"
- **Description**: "Core ticket aggregate with lifecycle management and state transitions"
- **Category**: "Domain Entity"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `ticket`
  - `domain`
  - `entity`

#### Files (`CodeFile[]`)

- **Name**: "ticket.py"
- **Path**: "app/ticket/domain/entities/ticket.py"
- **Language**: "python"
- **Content**:
  ```python
  class Ticket(BaseModel):
      showtime_id: int
      movie_id: int
      price_details: PriceDetails
      ticket_type: TicketType
      payment_details: Optional[PaymentDetails] = None
      seats: List[ShowtimeSeat] = Field(default_factory=list)
      customer_details: Optional[CustomerDetails] = None
      status: TicketStatus = TicketStatus.RESERVED
      id: int = 0
      created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
      updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

      def cancel_ticket(self) -> None:
          self.status = TicketStatus.CANCELLED
          self.updated_at = datetime.now(timezone.utc)

      def use_ticket(self) -> None:
          self.status = TicketStatus.USED
          self.updated_at = datetime.now(timezone.utc)

      def is_cancelable(self) -> bool:
          return True

      @staticmethod
      def max_seats_allowed_per_ticket() -> int:
          return MAX_LIMIT_OF_SEATS_PER_TICKET  # 12
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Ticket entity encapsulates ticket state and behavior, following domain-driven design principles with value objects for price and customer details."

---

### Example 3: Seat Management (`CodeExample`)

- **ID**: "seat-management"
- **Title**: "Showtime Seat Entity"
- **Description**: "Per-showtime seat entity with availability tracking and occupation logic"
- **Category**: "Domain Entity"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `seats`
  - `domain`
  - `availability`

#### Files (`CodeFile[]`)

- **Name**: "seats.py"
- **Path**: "app/ticket/domain/entities/seats.py"
- **Language**: "python"
- **Content**:
  ```python
  class ShowtimeSeat(BaseModel):
      showtime_id: int = Field(gt=0)
      seat_id: int = Field(gt=0)
      seat_name: str = Field(description="e.g., 'C4', 'F11'")
      is_available: bool = True
      created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
      taken_at: Optional[datetime] = None
      ticket_id: Optional[int] = None
      id: Optional[int] = None

      def ocuppy(self) -> None:
          if not self.is_available:
              raise SeatUnavailableError(self.id, "already taken")
          self.taken_at = datetime.now(timezone.utc)
          self.is_available = False

      def release(self) -> None:
          self.taken_at = None
          self.is_available = True
          self.ticket_id = None
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "ShowtimeSeat tracks individual seat availability per showtime with atomic occupation logic."

---

### Example 4: Repository Pattern (`CodeExample`)

- **ID**: "repository-pattern"
- **Title**: "SQLAlchemy Ticket Repository"
- **Description**: "PostgreSQL-backed repository implementation with async SQLAlchemy"
- **Category**: "Repository"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `repository`
  - `sqlalchemy`
  - `postgresql`

#### Files (`CodeFile[]`)

- **Name**: "sqlalchemy_ticket_repository.py"
- **Path**: "app/ticket/infrastructure/persistence/repository/sqlalchemy_ticket_repository.py"
- **Language**: "python"
- **Content**:
  ```python
  class SqlAlchemyTicketRepository(TicketRepository):
      def __init__(self, session: AsyncSession):
          self.session = session

      async def search(self, search_params: SearchTicketParams) -> List[Ticket]:
          stmt = select(TicketModel)
          
          # Apply filters
          if search_params.movie_id:
              stmt = stmt.where(TicketModel.movie_id == search_params.movie_id)
          if search_params.status:
              stmt = stmt.where(TicketModel.status == search_params.status.value)
          # ... more filters

          # Sorting
          sort_column = {
              "created_at": TicketModel.created_at,
              "price": TicketModel.price,
          }.get(search_params.sort_by, TicketModel.created_at)
          
          stmt = stmt.order_by(sort_column.asc() if search_params.sort_direction_asc else sort_column.desc())
          stmt = stmt.limit(search_params.page_limit).offset(search_params.page_offset)

          result = await self.session.execute(stmt)
          return [self._model_to_entity(model) for model in result.scalars().all()]
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "The repository implements async SQLAlchemy with proper filtering, sorting, and pagination support."

---

### Example 5: QR Code Generation (`CodeExample`)

- **ID**: "qr-generation"
- **Title**: "Ticket QR Code Generation"
- **Description**: "Generate QR codes with ticket ID and expiration for venue validation"
- **Category**: "Utility"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `qr`
  - `ticket`
  - `validation`

#### Files (`CodeFile[]`)

- **Name**: "qr.py"
- **Path**: "app/shared/qr.py"
- **Language**: "python"
- **Content**:
  ```python
  def generate_ticket_qr(ticket_id: str, expiration_date: datetime) -> str:
      qr_data = {
          "ticket_id": ticket_id,
          "expires_at": expiration_date.isoformat(),
          "version": "1.0",
      }
      
      qr = qrcode.QRCode(
          version=1,
          error_correction=ERROR_CORRECT_L,
          box_size=10,
          border=4,
      )
      
      qr.add_data(json.dumps(qr_data))
      qr.make(fit=True)
      
      img = qr.make_image(fill_color="black", back_color="white")
      
      buffered = io.BytesIO()
      img.save(buffered, "PNG")
      qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
      
      return f"data:image/png;base64,{qr_code_base64}"
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "QR codes contain ticket metadata for venue entry scanning, with version field for future compatibility."

---

### Example 6: Kafka Consumer (`CodeExample`)

- **ID**: "kafka-consumer"
- **Title**: "Billboard Event Consumer"
- **Description**: "Kafka consumer loop for processing billboard service events with deduplication"
- **Category**: "Integration"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - `kafka`
  - `consumer`
  - `event-driven`

#### Files (`CodeFile[]`)

- **Name**: "kafka_config.py"
- **Path**: "app/config/kafka_config.py"
- **Language**: "python"
- **Content**:
  ```python
  async def _run_billboard_consumer_loop(stop: asyncio.Event) -> None:
      service = await _build_billboard_replication_service()
      
      consumer = KafkaConsumer(
          settings.KAFKA_TOPIC_BILLBOARD_EVENTS,
          group_id=settings.KAFKA_CONSUMER_GROUP_BILLBOARD,
          enable_auto_commit=False,
          auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
      )
      
      try:
          while not stop.is_set():
              records = await loop.run_in_executor(
                  None, lambda: consumer.poll(timeout_ms=poll_ms)
              )
              for _tp, messages in records.items():
                  for msg in messages:
                      data = json.loads(msg.value.decode("utf-8"))
                      await service.apply_envelope(data)
                      await loop.run_in_executor(None, consumer.commit)
      finally:
          await loop.run_in_executor(None, consumer.close)
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "The consumer implements at-least-once delivery with manual offset commits after successful processing."
