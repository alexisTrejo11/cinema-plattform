# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Ticket Purchase Flow

- **ID**: "ticket-purchase"
- **Title**: "Digital Ticket Purchase"
- **Description**: Complete ticket purchase workflow including seat validation, payment authorization via gRPC, and QR code generation for venue entry.
- **Icon**: "ticket"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Atomic seat reservation with local and gRPC validation
  - Payment gateway integration via gRPC with idempotency support
  - QR code generation with expiration date
  - Transaction tracking with payment details
- **Tech Stack** (optional):
  - FastAPI
  - gRPC (grpcio)
  - Pydantic
  - QRCode library
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Purchase Success Rate"
  - **Value**: "99.5%"
  - **Trend** (optional): `up`
  - **Icon** (optional): "check-circle"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "ticket_command_use_cases.py"
  - **Code**:
    ```python
    class DigitalBuyTicketsUseCase:
        async def execute(self, buy_dto: BuyTicketsRequest) -> TicketPurchasedDetails:
            # 1. Load showtime + seats from local replica
            # 2. Validate seat availability locally
            # 3. Call billboard gRPC for authoritative check
            # 4. Call payment gRPC for authorization
            # 5. Take seats and persist ticket
            # 6. Generate QR code and return confirmation
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 2: Ticket Lifecycle Management

- **ID**: "ticket-lifecycle"
- **Title**: "Ticket Status Management"
- **Description**: Manage ticket lifecycle from purchase through cancellation or usage with proper state transitions.
- **Icon**: "sync"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Cancel tickets and release seats
  - Mark tickets as used (QR scan at venue)
  - Status tracking: reserved, purchased, used, cancelled, refunded
- **Tech Stack** (optional):
  - SQLAlchemy async
  - PostgreSQL
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Cancellation Rate"
  - **Value**: "5%"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "trending-down"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "ticket.py"
  - **Code**:
    ```python
    class TicketStatus(str, Enum):
        RESERVED = "reserved"
        USED = "used"
        REFUND = "refunded"
        NOT_USED = "not used"
        CANCELLED = "cancelled"
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 3: Seat Management

- **ID**: "seat-management"
- **Title**: "Showtime Seat Management"
- **Description**: Per-showtime seat inventory management with availability tracking and seat-specific reservations.
- **Icon**: "armchair"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Create seats from theater configuration
  - Atomic seat occupation with availability checks
  - Seat release on cancellation
  - Maximum 12 seats per ticket
- **Tech Stack** (optional):
  - SQLAlchemy async
  - PostgreSQL
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Seat Availability Accuracy"
  - **Value**: "99.9%"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "percent"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "seats.py"
  - **Code**:
    ```python
    class ShowtimeSeat(BaseModel):
        showtime_id: int
        seat_id: int
        seat_name: str
        is_available: bool = True
        
        def ocuppy(self):
            if not self.is_available:
                raise SeatUnavailableError(...)
            self.taken_at = datetime.now(timezone.utc)
            self.is_available = False
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 4: Ticket Search & Queries

- **ID**: "ticket-search"
- **Title**: "Advanced Ticket Search"
- **Description**: Rich ticket querying with filtering by movie, showtime, user, status, date range, and price range with pagination.
- **Icon**: "search"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Filter by movie, showtime, user, status
  - Date range filtering
  - Price range filtering
  - Pagination with limit/offset
  - Sort by created_at, updated_at, or price
- **Tech Stack** (optional):
  - SQLAlchemy async
  - Pydantic
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Search Response Time"
  - **Value**: "<100ms"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "clock"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "dtos.py"
  - **Code**:
    ```python
    class SearchTicketParams(BaseModel):
        movie_id: Optional[int] = None
        showtime_id: Optional[int] = None
        user_id: Optional[int] = None
        status: Optional[TicketStatus] = None
        created_before: Optional[datetime] = None
        created_after: Optional[datetime] = None
        price_min: Optional[float] = None
        price_max: Optional[float] = None
        page_limit: int = Field(default=10, ge=1, le=100)
        page_offset: int = Field(default=0, ge=0)
        sort_by: str = Field(default="created_at")
        sort_direction_asc: bool = True
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 5: Purchase Quote

- **ID**: "purchase-quote"
- **Title**: "Price Quote Generation"
- **Description**: Calculate price quotes for showtime tickets based on seat count, using replicated showtime data from MongoDB.
- **Icon**: "dollar-sign"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Read-only price calculation
  - No seat reservation during quote
  - Unit price and total calculation
  - Movie and showtime details included
- **Tech Stack** (optional):
  - MongoDB (Motor)
  - Pydantic
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Quotes Generated"
  - **Value**: "10K/day"
  - **Trend** (optional): `up`
  - **Icon** (optional): "trending-up"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "ticket_summary_use_cases.py"
  - **Code**:
    ```python
    class GetPurchaseQuoteUseCase:
        async def execute(self, showtime_id: int, seat_count: int) -> PurchaseQuoteResponse:
            showtime = await self.showtime_repository.get_by_id(showtime_id)
            unit = showtime.get_price()
            total = unit * seat_count
            return PurchaseQuoteResponse(..., unit_price=unit, total=total, ...)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 6: User Ticket Summary

- **ID**: "user-summary"
- **Title**: "User Ticket Dashboard"
- **Description**: Aggregated ticket statistics for user dashboards showing active, used, and cancelled ticket counts.
- **Icon**: "user"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Total tickets owned
  - Active (not used/cancelled) tickets
  - Used tickets count
  - Cancelled/refunded tickets count
- **Tech Stack** (optional):
  - SQLAlchemy async
  - PostgreSQL
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Average User Tickets"
  - **Value**: "3.5"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "users"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "ticket_summary_use_cases.py"
  - **Code**:
    ```python
    class GetUserTicketSummaryUseCase:
        async def execute(self, user_id: int) -> TicketSummaryResponse:
            tickets = await self.ticket_service.get_user_tickets(user_id)
            active = sum(1 for t in tickets if t.status in (RESERVED, NOT_USED))
            used = sum(1 for t in tickets if t.status == USED)
            cancelled = sum(1 for t in tickets if t.status in (CANCELLED, REFUND))
            return TicketSummaryResponse(user_id, total, active, used, cancelled)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 7: Event-Driven Data Replication

- **ID**: "kafka-replication"
- **Title**: "Billboard Event Replication"
- **Description**: Consume Kafka events from billboard service to replicate cinema, theater, and showtime data to MongoDB.
- **Icon**: "refresh-cw"
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Consume billboard.events topic
  - Idempotent processing via event deduplication
  - Process cinema.upserted, theater.upserted, showtime.upserted events
  - Handle showtime.cancelled events
- **Tech Stack** (optional):
  - Kafka-python
  - MongoDB (Motor)
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Event Processing Rate"
  - **Value**: "1000/sec"
  - **Trend** (optional): `up`
  - **Icon** (optional): "activity"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "kafka_config.py"
  - **Code**:
    ```python
    async def _run_billboard_consumer_loop(stop: asyncio.Event) -> None:
        consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_BILLBOARD_EVENTS,
            group_id=settings.KAFKA_CONSUMER_GROUP_BILLBOARD,
        )
        while not stop.is_set():
            records = await loop.run_in_executor(
                None, lambda: consumer.poll(timeout_ms=poll_ms)
            )
            for _tp, messages in records.items():
                for msg in messages:
                    data = json.loads(msg.value.decode("utf-8"))
                    await service.apply_envelope(data)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 8: JWT Authentication

- **ID**: "jwt-auth"
- **Title**: "JWT Bearer Token Authentication"
- **Description**: Optional JWT validation middleware supporting configurable audience, issuer, and algorithm with role-based access support.
- **Icon**: "shield"
- **Category** (`FeatureCategory`): `authentication`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Optional Bearer token validation
  - Configurable JWT settings (audience, issuer, algorithm)
  - Role-based authorization support
  - User context extraction from claims
- **Tech Stack** (optional):
  - PyJWT
  - FastAPI middleware
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Auth Success Rate"
  - **Value**: "99.8%"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "check"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "jwt_security.py"
  - **Code**:
    ```python
    class JwtAuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                claims = decode_jwt_token(token)
                request.state.current_user = AuthUserContext.from_claims(claims)
            return await call_next(request)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 9: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: "API Rate Limiting"
- **Description**: Per-client IP rate limiting using SlowAPI with different limits for different endpoint types.
- **Icon**: "sliders"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Purchase endpoints: 10/minute
  - Cancel/Use endpoints: 30/minute
  - Query endpoints: 60-120/minute
  - Default fallback: 60/minute
- **Tech Stack** (optional):
  - SlowAPI
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Rate Limit Violations"
  - **Value**: "0.1%"
  - **Trend** (optional): `down`
  - **Icon** (optional): "alert-triangle"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "ticket_command_controller.py"
  - **Code**:
    ```python
    @router.post("/buy", ...)
    @limiter.limit("10/minute")
    async def buy_tickets(request: Request, ...):
        ...
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 10: QR Code Generation

- **ID**: "qr-generation"
- **Title**: "Ticket QR Code"
- **Description**: Generate QR codes containing ticket ID and expiration date for venue entry validation.
- **Icon**: "qr-code"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Base64 encoded PNG QR codes
  - Includes ticket_id and expiration timestamp
  - Version field for future compatibility
  - Error correction (ERROR_CORRECT_L)
- **Tech Stack** (optional):
  - qrcode library
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "QR Generation Time"
  - **Value**: "<50ms"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "zap"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "qr.py"
  - **Code**:
    ```python
    def generate_ticket_qr(ticket_id: str, expiration_date: datetime) -> str:
        qr_data = {
            "ticket_id": ticket_id,
            "expires_at": expiration_date.isoformat(),
            "version": "1.0",
        }
        qr = qrcode.QRCode(version=1, error_correction=ERROR_CORRECT_L)
        qr.add_data(json.dumps(qr_data))
        img = qr.make_image(fill_color="black", back_color="white")
        return f"data:image/png;base64,{base64.b64encode(...)}"
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 11: Global Exception Handling

- **ID**: "exception-handling"
- **Title**: "Structured Error Responses"
- **Description**: Consistent error response format with proper HTTP status codes, error codes, and structured details.
- **Icon**: "alert-circle"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - DomainException -> 4xx with safe messages
  - ApplicationException -> 5xx with hidden internal details
  - Validation errors -> 422 with field-level details
  - Database errors -> 503 with generic message
- **Tech Stack** (optional):
  - FastAPI exception handlers
  - Pydantic
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Error Response Time"
  - **Value**: "<10ms"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "zap"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "global_exception_handler.py"
  - **Code**:
    ```python
    async def handle_domain_exceptions(request, exc: DomainException):
        return _error_response(
            status_code=exc.status_code,
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
        )
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 12: Structured Logging

- **ID**: "structured-logging"
- **Title**: "Structured Logging with Correlation"
- **Description**: JSON-structured logging with correlation IDs, custom log levels, and structured props for observability.
- **Icon**: "file-text"
- **Category** (`FeatureCategory`): `monitoring`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - JSON log format with timestamps
  - Custom props for business events
  - Request/response logging middleware
  - Separate app and audit logs
- **Tech Stack** (optional):
  - Python logging
  - colorlog
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Log Volume"
  - **Value**: "1GB/day"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "database"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "logging.py"
  - **Code**:
    ```python
    _log.info(
        "ticket_buy_completed",
        extra={
            "props": {
                "ticket_id": ticket_created.id,
                "showtime_id": buy_dto.showtime_id,
            }
        },
    )
    ```
- **GitHub Example URL** (optional): ""
