# Payment Service Kafka + gRPC Integration Guide

This guide explains how `payment-service` publishes and consumes Kafka events, and how to align gRPC contracts across services in this monorepo.

The implementation is intentionally simple (KISS): small event envelope, explicit topics, minimal incoming handlers.

---

## 1) Current integration points

### Outgoing Kafka events

`payment-service` publishes to:

- `KAFKA_TOPIC_PAYMENT_EVENTS` (default: `payment.events`)

Envelope shape:

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

Published from use cases through `PaymentEventsPublisher` port:

- `payment.intent.created`
- `payment.completed`
- `payment.failed`
- `payment.refunded`
- `payment.status.overridden`
- and other operational events introduced in admin/staff flows

### Incoming Kafka events

`payment-service` consumes from:

- `KAFKA_TOPIC_PAYMENT_INCOMING` (default: `payment.incoming`)

Handled event types:

- `payment.external.confirmed`
- `stripe.payment_intent.succeeded`
- `payment.external.failed`
- `stripe.payment_intent.failed`
- `show.cancelled`

Behavior:

- Confirm/fail events update local payment status.
- `show.cancelled` auto-refunds matching show payments when refundable.

---

## 2) Files added/updated

- `app/payments/infrastructure/messaging/kafka_payment_events.py`
  - Kafka producer adapter (`KafkaPaymentEventsPublisher`)
  - Inbound consumer (`PaymentInboundKafkaConsumer`)
- `app/payments/application/services/payment_incoming_events_handler.py`
  - Incoming event orchestration logic
- `app/config/kafka_config.py`
  - Startup/shutdown wiring for payment consumer tasks
- `app/payments/presentation/depencies.py`
  - Selects Kafka publisher adapter and gRPC assertion placeholder adapter
- `app/config/app_config.py`
  - Payment topic/group settings
- `proto/payment_contracts.proto`
  - Shared gRPC contract starter

---

## 3) Required env vars

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

Optional (for future real gRPC assertions):

```env
GRPC_BILLBOARD_TARGET=billboard-service:50051
GRPC_PAYMENT_TARGET=payment-service:50055
```

---

## 4) Monorepo Kafka setup (parent folder)

Because infrastructure lives in the same parent folder, define broker + topics in your root compose/infra stack.

Minimum recommendation:

- `kafka` service reachable as `kafka:9092` from containers
- topics created at startup:
  - `payment.events`
  - `payment.incoming`

If you use a topic-init job/container, keep it idempotent (create-if-not-exists).

---

## 5) How other services integrate

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

## 6) gRPC contract bootstrap

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

## 7) Keep it simple (current design choices)

- No schema registry yet.
- No DLQ flow yet (can be added later).
- No hard dependency on gRPC assertions yet (placeholder returns allowed).
- Incoming event handling is explicit and small; extend only when contracts are stable.

---

## 8) Suggested next incremental steps

1. Add integration tests for:
   - publish envelope shape
   - incoming `show.cancelled` auto-refund path
2. Add idempotency key handling for incoming events.
3. Add dead-letter topic for failed incoming events.
4. Replace placeholder gRPC client logic with generated stub calls.
