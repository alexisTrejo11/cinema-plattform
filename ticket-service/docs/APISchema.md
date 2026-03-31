# API Schema

- **Type**: `REST` | `GraphQL` | `SOAP` | `Mixed`

REST API (FastAPI) with OpenAPI/Swagger documentation

---

## HTTP Endpoints (`ApiEndpoint[]`)

### Endpoint 1

- **ID**: "buy-tickets"
- **Method**: `POST`
- **URL Path**: `/api/v2/tickets/buy`
- **Summary**: "Purchase tickets"
- **Description**: Creates a ticket after validating seats and payment context. Returns confirmation details including a QR payload for venue entry.
- **Tags**:
  - `Tickets — commands`
- **Authenticated**: `false` (JWT optional via middleware)
- **Rate Limit**: `10/minute`

#### Parameters (`ApiParameter[]`, optional)

For each parameter:

- **Name**: `request`
- **In**: `body`
- **Type**: `BuyTicketsRequest`
- **Required**: `true`
- **Description**: Purchase request with user details, showtime, seats, and payment info
- **Example** (optional): 

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: `application/json`
- **Schema**: `BuyTicketsRequest`
- **Example**:
  ```json
  {
    "user_email": "customer@example.com",
    "customer_id": 12345,
    "showtime_id": 789,
    "seat_list_id": [101, 102, 103],
    "payment_method": "credit_card",
    "ticket_type": "VIP",
    "payment_details": "tok_1JX9Z2KZJZJZJZJZJZJZJZJZ",
    "customer_ip": "192.168.1.1"
  }
  ```

#### Responses (`ApiResponse[]`)

For each response:

- **Status**: `201`
- **Description**: "Ticket created successfully."
- **Schema**: `TicketBuyedResponse`
- **Example**:
  ```json
  {
    "ticket_id": 12345,
    "transaction_id": "txn_1JX9Z2KZJZJZJZJZJZJZJZJZ",
    "movie_name": "The Matrix Resurrections",
    "cinema_name": "Cineplex Downtown",
    "theater_name": "Screen 4",
    "showtime_date": "2023-12-25T19:30:00Z",
    "ticket_qr": "data:image/png;base64,iVBORw0KGgo...",
    "seats": [
      {"id": 101, "seat_number": "F12", "row": "F", "number": 12, "type": "Standard"}
    ]
  }
  ```

---

### Endpoint 2

- **ID**: "cancel-ticket"
- **Method**: `PATCH`
- **URL Path**: `/api/v2/tickets/{ticket_id}/cancel`
- **Summary**: "Cancel a ticket"
- **Description**: Marks the ticket as cancelled and releases associated seats when applicable. Idempotent only when business rules allow repeated cancel.
- **Tags**:
  - `Tickets — commands`
- **Authenticated**: `false`
- **Rate Limit**: `30/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `ticket_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Primary key of the ticket to cancel"
- **Example** (optional): `12345`

#### Responses (`ApiResponse[]`)

- **Status**: `204`
- **Description**: "Operation succeeded; no response body."
- **Schema**: ``
- **Example**:
  ```json
  {}
  ```

---

### Endpoint 3

- **ID**: "use-ticket"
- **Method**: `PATCH`
- **URL Path**: `/api/v2/tickets/{ticket_id}/use`
- **Summary**: "Mark ticket as used"
- **Description**: Marks the ticket as used (e.g. after QR scan at the door). Cannot be applied to cancelled or already-used tickets.
- **Tags**:
  - `Tickets — commands`
- **Authenticated**: `false`
- **Rate Limit**: `30/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `ticket_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Primary key of the ticket to mark as used"
- **Example** (optional): `12345`

#### Responses (`ApiResponse[]`)

- **Status**: `204`
- **Description**: "Operation succeeded; no response body."

---

### Endpoint 4

- **ID**: "get-user-ticket-summary"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/user/{user_id}/summary`
- **Summary**: "Ticket counts for a user"
- **Description**: Aggregated totals for dashboard / account pages (active, used, cancelled).
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `60/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `user_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "User id"
- **Example** (optional): `42`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Summary statistics for the user."
- **Schema**: `TicketSummaryResponse`
- **Example**:
  ```json
  {
    "user_id": 42,
    "total_tickets": 12,
    "active_tickets": 5,
    "used_tickets": 4,
    "cancelled_tickets": 3
  }
  ```

---

### Endpoint 5

- **ID**: "get-purchase-quote"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/quotes/showtime/{showtime_id}`
- **Summary**: "Price quote for a showtime"
- **Description**: Read-only price preview from the replicated showtime (Mongo). Does not hold seats or create a reservation.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `120/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `showtime_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Showtime identifier"
- **Example** (optional): `101`

- **Name**: `seat_count`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Number of seats to price"
- **Example** (optional): `2`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Computed unit and total price for the requested seat count."
- **Schema**: `PurchaseQuoteResponse`
- **Example**:
  ```json
  {
    "showtime_id": 101,
    "seat_count": 2,
    "unit_price": "12.50",
    "currency": "USD",
    "total": "25.00",
    "movie_title": "Dune",
    "showtime_starts_at": "2025-06-01T20:00:00Z"
  }
  ```

---

### Endpoint 6

- **ID**: "list-showtime-seats"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/showtime/{showtime_id}/seats`
- **Summary**: "Seats available for a showtime"
- **Description**: Seat map / availability derived from theater replica and showtime seat rows.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `120/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `showtime_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Showtime identifier"
- **Example** (optional): `789`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "List of seats with row, number, and type."
- **Schema**: `List[SeatInfo]`
- **Example**:
  ```json
  [
    {"id": 1, "seat_number": "A12", "row": "A", "number": 12, "type": "VIP"}
  ]
  ```

---

### Endpoint 7

- **ID**: "search-tickets"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/`
- **Summary**: "Search tickets"
- **Description**: Filter and paginate tickets using optional movie, showtime, user, status, and date-range criteria.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `60/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `movie_id`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Filter by movie ID"

- **Name**: `showtime_id`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Filter by showtime ID"

- **Name**: `user_id`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Filter by purchaser user ID"

- **Name**: `status`
- **In**: `query`
- **Type**: `string`
- **Required**: `false`
- **Description**: "Filter by ticket lifecycle status"

- **Name**: `page_limit`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Page size (1-100)"

- **Name**: `page_offset`
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Offset for pagination"

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Matching tickets (may be empty)."
- **Schema**: `List[TicketResponse]`
- **Example**:
  ```json
  [
    {
      "id": 123,
      "user_id": 456,
      "movie_id": 789,
      "showtime_id": 101,
      "price": 12.50,
      "price_currency": "USD",
      "status": "purchased",
      "created_at": "2023-01-01T12:00:00Z",
      "seats": []
    }
  ]
  ```

---

### Endpoint 8

- **ID**: "get-ticket-by-id"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/{ticket_id}`
- **Summary**: "Get ticket by ID"
- **Description**: Returns one ticket with optional seat breakdown when stored.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `120/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `ticket_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Ticket primary key"
- **Example** (optional): `123`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Ticket payload."
- **Schema**: `TicketResponse`

---

### Endpoint 9

- **ID**: "list-user-tickets"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/user/{user_id}`
- **Summary**: "List tickets for a user"
- **Description**: Returns tickets owned by the user, newest first when supported by the repository.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `60/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `user_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "User id"
- **Example** (optional): `456`

- **Name**: `include_seats`
- **In**: `query`
- **Type**: `boolean`
- **Required**: `false`
- **Description**: "Include seat information on each ticket"
- **Example** (optional): `true`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Zero or more tickets."
- **Schema**: `List[TicketResponse]`

---

### Endpoint 10

- **ID**: "list-showtime-tickets"
- **Method**: `GET`
- **URL Path**: `/api/v2/tickets/showtime/{showtime_id}`
- **Summary**: "List tickets for a showtime"
- **Description**: Useful for box office / capacity checks; may include seat payloads.
- **Tags**:
  - `Tickets — queries`
- **Authenticated**: `false`
- **Rate Limit**: `60/minute`

#### Parameters (`ApiParameter[]`, optional)

- **Name**: `showtime_id`
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "Showtime id"
- **Example** (optional): `789`

- **Name**: `include_seats`
- **In**: `query`
- **Type**: `boolean`
- **Required**: `false`
- **Description**: "Include seat information on each ticket"
- **Example** (optional): `true`

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Zero or more tickets for the showtime."
- **Schema**: `List[TicketResponse]`

---

### Endpoint 11

- **ID**: "health-check"
- **Method**: `GET`
- **URL Path**: `/health`
- **Summary**: "Health check"
- **Description**: Returns service health status
- **Tags**:
  - `Health`
- **Authenticated**: `false`
- **Rate Limit**: None

#### Responses (`ApiResponse[]`)

- **Status**: `200`
- **Description**: "Service health status"
- **Schema**:
- **Example**:
  ```json
  {"status": "healthy", "service": "ticket-service"}
  ```
