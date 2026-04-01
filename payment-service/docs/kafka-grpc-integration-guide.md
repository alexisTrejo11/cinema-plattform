# Payment Service Kafka + gRPC Integration Guide

**Service**: payment-service  
**Version**: 2.0.0  
**Last Updated**: 2026-04-01

This guide explains how `payment-service` publishes and consumes Kafka events, and how to align gRPC contracts across services in this monorepo.

The implementation is intentionally simple (KISS): small event envelope, explicit topics, minimal incoming handlers.

---

## 1) Service Overview

| Property | Value |
|----------|-------|
| REST API Port | 8000 |
| gRPC Port | 50055 |
| Kafka Topics | `payment.events`, `payment.incoming` |
| Consumer Group | `payment-service-consumer` |
| Database | PostgreSQL (cinema_payments) |

---

## 2) Current Integration Points

### Outgoing Kafka Events

`payment-service` publishes to:

- `KAFKA_TOPIC_PAYMENT_EVENTS` (default: `payment.events`)

#### Event Envelope Structure

```json
{
  "event_type": "payment.intent.created",
  "service": "payment-service",
  "payload": {
    "payment_id": "uuid",
    "user_id": "uuid"
  }
}
```

#### Published Event Types

Published from use cases through `PaymentEventsPublisher` port:

| Event Type | Trigger |
|------------|---------|
| `payment.intent.created` | New payment created |
| `payment.processing_started` | Payment processing begins |
| `payment.completed` | Payment successful |
| `payment.failed` | Payment failed |
| `payment.cancelled` | Payment cancelled |
| `payment.refunded` | Refund processed |
| `payment.status.overridden` | Admin status override |
| `payment.refund.staff_requested` | Staff refund request |
| `stripe.webhook.*` | Stripe webhook events |
| `transaction.reverse.requested` | Transaction reversal request |

### Incoming Kafka Events

`payment-service` consumes from:

- `KAFKA_TOPIC_PAYMENT_INCOMING` (default: `payment.incoming`)

#### Consumed Event Types

| Event Type | Action |
|------------|--------|
| `payment.external.confirmed` | Mark payment completed |
| `stripe.payment_intent.succeeded` | Mark payment completed |
| `payment.external.failed` | Mark payment failed |
| `stripe.payment_intent.failed` | Mark payment failed |
| `show.cancelled` | Auto-refund matching payments |

#### Incoming Event Handling Behavior

- Confirm/fail events update local payment status
- `show.cancelled` auto-refunds matching show payments when refundable

---

## 3) Implementation Files

| File | Description |
|------|-------------|
| `app/payments/infrastructure/messaging/kafka_payment_events.py` | Kafka producer adapter, inbound consumer |
| `app/payments/application/services/payment_incoming_events_handler.py` | Incoming event orchestration |
| `app/config/kafka_config.py` | Startup/shutdown wiring for consumers |
| `app/payments/presentation/depencies.py` | Adapter selection (Kafka, gRPC) |
| `app/config/app_config.py` | Kafka topic/group settings |
| `proto/payment_contracts.proto` | Shared gRPC contracts |

---

## 4) Environment Variables

### Required for Kafka

Add these to `payment-service/.env`:

```env
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_CLIENT_ID=payment-service

KAFKA_CONSUMER_ENABLED=true
KAFKA_CONSUMER_PAYMENT_ENABLED=true
KAFKA_CONSUMER_GROUP_PAYMENT=payment-service-consumer
KAFKA_CONSUMER_AUTO_OFFSET_RESET=latest
KAFKA_CONSUMER_POLL_TIMEOUT_MS=1000

KAFKA_TOPIC_PAYMENT_EVENTS=payment.events
KAFKA_TOPIC_PAYMENT_INCOMING=payment.incoming
```

### Optional for gRPC

```env
GRPC_BILLBOARD_TARGET=billboard-service:50051
GRPC_PAYMENT_TARGET=payment-service:50055
```

---

## 5) Monorepo Kafka Setup

Because infrastructure lives in the same parent folder, define broker + topics in your root compose/infra stack.

### Minimum Requirements

- `kafka` service reachable as `kafka:9092` from containers
- Topics created at startup:
  - `payment.events`
  - `payment.incoming`

If you use a topic-init job/container, keep it idempotent (create-if-not-exists).

---

## 6) How Other Services Integrate

### Consume payment events

Other services should subscribe to `payment.events` and filter by `event_type`.

Common useful events:

- `payment.intent.created`
- `payment.completed`
- `payment.failed`
- `payment.refunded`

### Send events to payment service

Other services publish to `payment.incoming` using the same envelope:

```json
{
  "event_type": "show.cancelled",
  "service": "billboard-service",
  "payload": {
    "show_id": "show_123"
  }
}
```

---

## 7) gRPC Contract Bootstrap

Proto file:

- `proto/payment_contracts.proto`

It includes:

- `PurchaseAssertionService`
  - ticket/concessions/merchandise/subscription/wallet assertions
- `PaymentQueryService`
  - get payment status
- `PaymentEventEnvelope`
  - reusable envelope message

Generate Python stubs:

```bash
python -m grpc_tools.protoc \
  -I ./proto \
  --python_out=./app/payments/infrastructure/grpc/generated \
  --grpc_python_out=./app/payments/infrastructure/grpc/generated \
  ./proto/payment_contracts.proto
```

Create the output folder first if needed.

---

## 8) Design Principles

- No schema registry yet.
- No DLQ flow yet (can be added later).
- No hard dependency on gRPC assertions yet (placeholder returns allowed).
- Incoming event handling is explicit and small; extend only when contracts are stable.

---

## 9) Suggested Next Steps

1. Add integration tests for:
   - publish envelope shape
   - incoming `show.cancelled` auto-refund path
2. Add idempotency key handling for incoming events.
3. Add dead-letter topic for failed incoming events.
4. Replace placeholder gRPC client logic with generated stub calls.