# API Schema

- **Type**: `REST`

---

## HTTP Endpoints (`ApiEndpoint[]`)

### Endpoint 1 - Create Notification

- **ID**: create-notification
- **Method**: `POST`
- **URL Path**: /api/v2/notifications
- **Summary**: Create a new notification
- **Description**: Creates a new notification, saves it to MongoDB, and sends it via the specified channel
- **Tags**:
  - notifications
- **Authenticated**: `true`
- **Rate Limit**: 60/minute

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: application/json
- **Schema**: 
  ```json
  {
    "notification_type": "TICKET_BUY | PRODUCT_BUY | ACCOUNT_AUTH | ACCOUNT_CREATED | ACCOUNT_DELETED | PAYMENT_FAILED | ANNOUNCEMENT | CUSTOM_MESSAGE",
    "channel": "EMAIL | SMS | PUSH_NOTIFICATION | IN_APP",
    "recipient": {
      "user_id": "string",
      "email": "string (optional)",
      "phone_number": "string (optional)"
    },
    "content": {
      "subject": "string",
      "body": "string",
      "template_name": "string (optional)",
      "data": "object (optional)"
    },
    "is_important": "boolean (optional, default: false)"
  }
  ```
- **Example**:
  ```json
  {
    "notification_type": "TICKET_BUY",
    "channel": "EMAIL",
    "recipient": {
      "user_id": "user-123",
      "email": "user@example.com"
    },
    "content": {
      "subject": "Your Ticket Confirmation",
      "body": "Your tickets have been purchased successfully. Movie: Avatar 2, Time: 7:00 PM"
    },
    "is_important": false
  }
  ```

#### Responses (`ApiResponse[]`)

- **Status**: 201
- **Description**: Notification created successfully
- **Schema** (optional): NotificationResponse
- **Example**:
  ```json
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440000",
    "notification_type": "TICKET_BUY",
    "channel": "EMAIL",
    "recipient": {
      "user_id": "user-123",
      "email": "user@example.com"
    },
    "content": {
      "subject": "Your Ticket Confirmation",
      "body": "Your tickets have been purchased successfully.",
      "template_name": null,
      "data": {}
    },
    "status": "SENT",
    "created_at": "2026-04-06T12:00:00Z",
    "sent_at": "2026-04-06T12:00:01Z",
    "is_important": false,
    "attention_status": "NONE"
  }
  ```

---

- **Status**: 401
- **Description**: Unauthorized - Invalid or missing JWT token
- **Schema** (optional): ErrorResponse
- **Example**:
  ```json
  {
    "error_code": "UNAUTHORIZED",
    "message": "Invalid authentication credentials"
  }
  ```

---

- **Status**: 422
- **Description**: Validation error
- **Schema** (optional): ErrorResponse
- **Example**:
  ```json
  {
    "error_code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [...]
  }
  ```

---

### Endpoint 2 - Get Notification by ID

- **ID**: get-notification
- **Method**: `GET`
- **URL Path**: /api/v2/notifications/{notification_id}
- **Summary**: Get notification by ID
- **Description**: Retrieves a single notification by its unique identifier
- **Tags**:
  - notifications
- **Authenticated**: `true`
- **Rate Limit**: 60/minute

#### Parameters (`ApiParameter[]`, optional)

- **Name**: notification_id
- **In**: `path`
- **Type**: string (UUID)
- **Required**: `true`
- **Description**: The unique notification identifier
- **Example** (optional): 550e8400-e29b-41d4-a716-446655440000

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: Notification found
- **Schema** (optional): NotificationResponse
- **Example**:
  ```json
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440000",
    "notification_type": "TICKET_BUY",
    "channel": "EMAIL",
    "recipient": {
      "user_id": "user-123",
      "email": "user@example.com"
    },
    "content": {
      "subject": "Your Ticket Confirmation",
      "body": "Your tickets have been purchased successfully.",
      "template_name": null,
      "data": {}
    },
    "status": "SENT",
    "created_at": "2026-04-06T12:00:00Z",
    "sent_at": "2026-04-06T12:00:01Z",
    "is_important": false,
    "attention_status": "NONE"
  }
  ```

---

- **Status**: 404
- **Description**: Notification not found
- **Schema** (optional): ErrorResponse
- **Example**:
  ```json
  {
    "error_code": "NOT_FOUND",
    "message": "Notification not found"
  }
  ```

---

### Endpoint 3 - List Notifications

- **ID**: list-notifications
- **Method**: `GET`
- **URL Path**: /api/v2/notifications
- **Summary**: List notifications with filters
- **Description**: Returns a paginated list of notifications with optional filtering
- **Tags**:
  - notifications
- **Authenticated**: `true`
- **Rate Limit**: 60/minute

#### Parameters (`ApiParameter[]`, optional)

- **Name**: notification_type
- **In**: `query`
- **Type**: string (enum)
- **Required**: `false`
- **Description**: Filter by notification type
- **Example** (optional): TICKET_BUY

---

- **Name**: channel
- **In**: `query`
- **Type**: string (enum)
- **Required**: `false`
- **Description**: Filter by channel
- **Example** (optional): EMAIL

---

- **Name**: user_id
- **In**: `query`
- **Type**: string
- **Required**: `false`
- **Description**: Filter by recipient user ID
- **Example** (optional): user-123

---

- **Name**: status
- **In**: `query`
- **Type**: string (enum)
- **Required**: `false`
- **Description**: Filter by notification status
- **Example** (optional): SENT

---

- **Name**: is_important
- **In**: `query`
- **Type**: boolean
- **Required**: `false`
- **Description**: Filter by importance flag
- **Example** (optional): true

---

- **Name**: attention_status
- **In**: `query`
- **Type**: string (enum)
- **Required**: `false`
- **Description**: Filter by attention status
- **Example** (optional): OPEN

---

- **Name**: source_event_type
- **In**: `query`
- **Type**: string
- **Required**: `false`
- **Description**: Filter by source event type
- **Example** (optional): ticket.purchased

---

- **Name**: limit
- **In**: `query`
- **Type**: integer
- **Required**: `false`
- **Description**: Number of results per page (1-100, default: 10)
- **Example** (optional): 10

---

- **Name**: offset
- **In**: `query`
- **Type**: integer
- **Required**: `false`
- **Description**: Number of results to skip (default: 0)
- **Example** (optional): 0

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: List of notifications
- **Schema** (optional): NotificationListResponse
- **Example**:
  ```json
  {
    "total": 100,
    "limit": 10,
    "offset": 0,
    "items": [
      {
        "notification_id": "550e8400-e29b-41d4-a716-446655440000",
        "notification_type": "TICKET_BUY",
        "channel": "EMAIL",
        "recipient": {
          "user_id": "user-123",
          "email": "user@example.com"
        },
        "content": {
          "subject": "Your Ticket Confirmation",
          "body": "Your tickets have been purchased successfully.",
          "template_name": null,
          "data": {}
        },
        "status": "SENT",
        "created_at": "2026-04-06T12:00:00Z",
        "sent_at": "2026-04-06T12:00:01Z",
        "is_important": false,
        "attention_status": "NONE"
      }
    ]
  }
  ```

---

### Endpoint 4 - Health Check

- **ID**: health-check
- **Method**: `GET`
- **URL Path**: /health
- **Summary**: Health check endpoint
- **Description**: Returns the health status of the service
- **Tags**:
  - health
- **Authenticated**: `false`
- **Rate Limit**: None

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: Service is healthy
- **Schema** (optional): {"status": "ok"}
- **Example**:
  ```json
  {
    "status": "ok"
  }
  ```

---

### Endpoint 5 - Ping

- **ID**: ping
- **Method**: `GET`
- **URL Path**: /ping
- **Summary**: Ping endpoint
- **Description**: Simple ping to check if service is alive
- **Tags**:
  - health
- **Authenticated**: `false`
- **Rate Limit**: None

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: Pong response
- **Schema** (optional): {"ping": "pong!"}
- **Example**:
  ```json
  {
    "ping": "pong!"
  }
  ```

---

## Enums

### NotificationType

| Value | Description |
|-------|-------------|
| PRODUCT_BUY | Product purchase notification |
| TICKET_BUY | Movie ticket purchase notification |
| ACCOUNT_AUTH | Authentication event (login, 2FA) |
| ACCOUNT_CREATED | New account registration |
| ACCOUNT_DELETED | Account deletion notification |
| PAYMENT_FAILED | Payment failure alert |
| ANNOUNCEMENT | Platform announcement |
| CUSTOM_MESSAGE | Custom notification message |

### NotificationChannel

| Value | Description |
|-------|-------------|
| EMAIL | Email via SMTP |
| SMS | SMS via Twilio |
| PUSH_NOTIFICATION | Mobile push notification |
| IN_APP | In-application notification |

### NotificationStatus

| Value | Description |
|-------|-------------|
| PENDING | Created, awaiting processing |
| SENT | Successfully sent to provider |
| FAILED | Delivery failed |
| DELIVERED | Confirmed delivered to user |
| READ | User has read notification |
| CANCELED | Notification canceled |

### NotificationAttentionStatus

| Value | Description |
|-------|-------------|
| NONE | No attention needed |
| OPEN | Requires operational follow-up |
| ACKNOWLEDGED | Attention acknowledged |
| RESOLVED | Issue resolved |
