# API Schema

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except health checks) require JWT Bearer token authentication.

```
Authorization: Bearer <jwt_token>
```

JWT Payload Requirements:
- `sub`: User ID (UUID)
- `roles`: Array of role strings (`admin`, `manager`, `employee`, `customer`)

---

## Endpoints

### Service Endpoints

#### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "payment-service"
}
```

---

### Customer Endpoints

#### Get Payment History

```
GET /api/v1/payments/customers/history
```

**Query Parameters:**
- `limit` (int, 1-100, default: 20)
- `offset` (int, min: 0, default: 0)

**Response:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "amount": 29.99,
    "currency": "USD",
    "status": "completed",
    "payment_method": "stripe",
    "payment_type": "ticket_purchase",
    "created_at": "2026-04-01T12:00:00Z",
    "updated_at": "2026-04-01T12:00:00Z",
    "completed_at": "2026-04-01T12:05:00Z"
  }
]
```

---

#### Get Payment Detail

```
GET /api/v1/payments/customers/payments/{payment_id}
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "amount": 29.99,
  "currency": "USD",
  "status": "completed",
  "payment_method": "stripe",
  "payment_type": "ticket_purchase",
  "created_at": "2026-04-01T12:00:00Z",
  "updated_at": "2026-04-01T12:00:00Z",
  "completed_at": "2026-04-01T12:05:00Z"
}
```

---

#### Purchase Tickets

```
POST /api/v1/payments/customers/tickets
```

**Request Body:**
```json
{
  "show_id": "uuid",
  "showtime_id": "uuid",
  "seats": ["A1", "A2"],
  "total_amount": 29.99,
  "currency": "USD",
  "payment_method": "stripe",
  "notes": "Optional notes"
}
```

**Response:** `PaymentResponse`

---

#### Purchase Concessions

```
POST /api/v1/payments/customers/consessions
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "items": [
    {"item_id": "popcorn_large", "name": "Large Popcorn", "quantity": 1, "price": 12.99}
  ],
  "total_amount": 22.99,
  "currency": "USD",
  "payment_method": "wallet"
}
```

**Response:** `PaymentResponse`

---

#### Purchase Merchandise

```
POST /api/v1/payments/customers/merchandise
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "items": [
    {"item_id": "tshirt_m", "name": "Movie T-Shirt", "quantity": 1, "price": 25.99}
  ],
  "total_amount": 25.99,
  "currency": "USD",
  "payment_method": "stripe"
}
```

**Response:** `PaymentResponse`

---

#### Purchase Subscription

```
POST /api/v1/payments/customers/subscriptions
```

**Request Body:**
```json
{
  "plan_id": "uuid",
  "period": "monthly",
  "total_amount": 9.99,
  "currency": "USD",
  "payment_method": "stripe"
}
```

**Response:** `PaymentResponse`

---

#### Add Wallet Credit

```
POST /api/v1/payments/customers/wallets/credit
```

**Request Body:**
```json
{
  "wallet_id": "uuid",
  "total_amount": 50.00,
  "currency": "USD",
  "payment_method": "stripe"
}
```

**Response:** `PaymentResponse`

---

#### Cancel Payment

```
POST /api/v1/payments/customers/payments/{payment_id}/cancel
```

**Request Body:**
```json
{
  "reason": "User requested cancellation"
}
```

**Response:** `PaymentResponse`

---

#### Request Refund

```
POST /api/v1/payments/customers/payments/{payment_id}/refund
```

**Request Body:**
```json
{
  "reason": "Customer refund request",
  "refund_amount": 15.00
}
```

**Response:** `PaymentResponse`

---

#### Get Receipt

```
GET /api/v1/payments/customers/payments/{payment_id}/receipt
```

**Response:**
```json
{
  "payment_id": "uuid",
  "status": "completed",
  "amount": 29.99,
  "currency": "USD",
  "issued_at": "2026-04-01T12:05:00Z",
  "receipt_url": "https://payments.local/receipts/uuid"
}
```

---

### Staff Endpoints

#### Verify Payment Status

```
GET /api/v1/payments/staff/{payment_id}/status
```

**Response:** `PaymentResponse`

---

#### Get Receipt

```
GET /api/v1/payments/staff/{payment_id}/receipt
```

**Response:** `ReceiptResponse`

---

#### Refund for Cancelled Show

```
POST /api/v1/payments/staff/{payment_id}/refund
```

**Request Body:**
```json
{
  "reason": "Show cancelled by theater"
}
```

**Response:** `PaymentResponse`

---

#### Get Payments by Show

```
GET /api/v1/payments/staff/show/{show_id}
```

**Query Parameters:**
- `limit` (int, 1-200, default: 100)
- `offset` (int, min: 0, default: 0)

**Response:** `List[PaymentResponse]`

---

#### Get Show Revenue Summary

```
GET /api/v1/payments/staff/show/{show_id}/summary
```

**Response:**
```json
{
  "show_id": "uuid",
  "payments_count": 150,
  "completed_count": 145,
  "gross_revenue": 4350.55,
  "refunded_revenue": 100.00,
  "net_revenue": 4250.55,
  "currency": "USD"
}
```

---

### Admin Endpoints

#### Search Payments

```
GET /api/v1/payments/admin/payments
```

**Query Parameters:**
- `user_id` (string, optional)
- `status` (string, optional)
- `limit` (int, 1-200, default: 50)
- `offset` (int, min: 0, default: 0)

**Response:** `List[PaymentResponse]`

---

#### Override Payment Status

```
PATCH /api/v1/payments/admin/payments/{payment_id}/status
```

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:** `PaymentResponse`

---

#### Force Refund

```
POST /api/v1/payments/admin/payments/{payment_id}/refund
```

**Request Body:**
```json
{
  "reason": "Admin-initiated refund",
  "refund_amount": 29.99
}
```

**Response:** `PaymentResponse`

---

#### Void Payment

```
POST /api/v1/payments/admin/payments/{payment_id}/void
```

**Request Body:**
```json
{
  "reason": "Payment voided by admin"
}
```

**Response:** `PaymentResponse`

---

#### Get Payments Summary

```
GET /api/v1/payments/admin/summary
```

**Response:**
```json
{
  "total": 1500,
  "by_status": {
    "completed": 1200,
    "pending": 200,
    "failed": 100
  },
  "gross_amount": 45000.00
}
```

---

#### Get Summary by Type

```
GET /api/v1/payments/admin/summary/by-type
```

**Response:**
```json
{
  "ticket_purchase": 25000.00,
  "food_purchase": 15000.00,
  "merchandise_purchase": 5000.00
}
```

---

#### Get Summary by Payment Method

```
GET /api/v1/payments/admin/summary/by-method
```

**Response:**
```json
{
  "stripe": 35000.00,
  "wallet": 10000.00
}
```

---

### Payment Method Catalog Endpoints

#### List Payment Methods

```
GET /api/v2/payment/methods/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Credit or debit card",
    "provider": "stripe",
    "type": "card",
    "stripe_code": "card",
    "is_active": true,
    "min_amount": 0.0,
    "created_at": "2026-03-01T00:00:00Z",
    "updated_at": "2026-03-01T00:00:00Z"
  }
]
```

---

#### Get Payment Method

```
GET /api/v2/payment/methods/{payment_method_id}
```

**Response:** `PaymentMethodResponse`

---

#### Create Payment Method

```
POST /api/v2/payment/methods/
```

**Request Body:**
```json
{
  "name": "Credit or debit card",
  "provider": "stripe",
  "type": "card",
  "stripe_code": "card",
  "is_active": true,
  "min_amount": 0.0
}
```

**Response:** `PaymentMethodResponse`

---

#### Update Payment Method

```
PUT /api/v2/payment/methods/{payment_method_id}
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "is_active": false
}
```

---

#### Restore Payment Method

```
POST /api/v2/payment/methods/{payment_method_id}/restore
```

---

#### Delete Payment Method

```
DELETE /api/v2/payment/methods/{payment_method_id}
```

---

## Response Schemas

### PaymentResponse

```json
{
  "id": "string (uuid)",
  "user_id": "string (uuid)",
  "amount": "number (float)",
  "currency": "string (3 chars)",
  "status": "string (enum: pending|processing|completed|failed|cancelled|refunded|partially_refunded)",
  "payment_method": "string",
  "payment_type": "string (enum: ticket_purchase|food_purchase|merchandise_purchase|wallet_topup|subscription)",
  "created_at": "datetime",
  "updated_at": "datetime",
  "completed_at": "datetime | null",
  "stripe_payment_intent_id": "string | null",
  "metadata": "object"
}
```

### PaymentMethodResponse

```json
{
  "id": "string (uuid)",
  "name": "string",
  "provider": "string (enum: stripe|paypal|adyen|internal)",
  "type": "string (enum: card|cash|bank|wallet)",
  "stripe_code": "string",
  "is_active": "boolean",
  "min_amount": "number (float)",
  "created_at": "datetime",
  "updated_at": "datetime",
  "deleted_at": "datetime | null"
}
```

### ReceiptResponse

```json
{
  "payment_id": "string (uuid)",
  "status": "string",
  "amount": "number (float)",
  "currency": "string (3 chars)",
  "issued_at": "datetime",
  "receipt_url": "string (url)"
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized

```json
{
  "detail": "Invalid or expired token."
}
```

### 403 Forbidden

```json
{
  "detail": "This action requires an admin role."
}
```

### 404 Not Found

```json
{
  "detail": "Payment not found"
}
```

### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "error message",
      "type": "value_error"
    }
  ]
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```
