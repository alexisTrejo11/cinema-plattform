# Shared event catalog (billboard + wallet)

This catalog defines **contract-first** Kafka events consumed by ticket-service (and potentially other services). Producers **must** increment `schema_version` or introduce a new `event_type` suffix for breaking changes.

## Message envelope (all events)

Every record is JSON with this wrapper (aligned with [BaseEvent](../app/shared/events/base.py) concepts):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | string (UUID) | yes | Unique id for idempotent consumption |
| `event_type` | string | yes | Stable type name (see tables below) |
| `schema_version` | integer | yes | Payload schema version (start at `1`) |
| `occurred_at` | string (ISO 8601 UTC) | yes | When the fact happened at the source |
| `service` | string | yes | Emitting service name (e.g. `billboard-service`) |
| `correlation_id` | string \| null | no | Trace across HTTP/Kafka |
| `payload` | object | yes | Event-specific body (see below) |

---

## Billboard-service events (`billboard.events` topic)

Partition key: see [kafka-topics.md](./kafka-topics.md).

### `cinema.upserted`

**`event_type`:** `cinema.upserted`  
**`schema_version`:** `1`

**`payload`:**

| Field | Type | Description |
|-------|------|-------------|
| `cinema_id` | integer | Stable cinema identifier |
| `name` | string | Display name |
| `address` | string | Full address |
| `is_active` | boolean | Whether the cinema accepts bookings |
| `theaters` | array | Embedded theater summaries **or** empty if theaters arrive via separate events (team choice) |
| `updated_at` | string (ISO 8601) | Source row version hint |

**Semantics:** Upsert the cinema document in Mongo `cinemas` (see [ticket-service-consumer-spec.md](./ticket-service-consumer-spec.md)).

---

### `cinema.deactivated`

**`event_type`:** `cinema.deactivated`  
**`schema_version`:** `1`

**`payload`:**

| Field | Type | Description |
|-------|------|-------------|
| `cinema_id` | integer | |
| `reason` | string \| null | Optional audit text |

**Semantics:** Mark cinema inactive or remove from replica per product rules.

---

### `theater.upserted`

**`event_type`:** `theater.upserted`  
**`schema_version`:** `1`

**`payload`:** Full theater aggregate including `theater_id`, `cinema_id`, `name`, `capacity`, `theater_type`, `seats[]` (seat_id, seat_row, seat_number, seat_type, is_active), flags, timestamps.

**Semantics:** Upsert into Mongo `theaters` and refresh nested references inside `cinemas` if your projection embeds theaters.

---

### `theater.deleted`

**`event_type`:** `theater.deleted`  
**`schema_version`:** `1`

**`payload`:**

| Field | Type | Description |
|-------|------|-------------|
| `theater_id` | integer | |
| `cinema_id` | integer | For partition routing and cleanup |

---

### `showtime.upserted`

**`event_type`:** `showtime.upserted`  
**`schema_version`:** `1`

**`payload`:** Snapshot aligned with ticket-service `Showtime` read model: `showtime_id`, nested or denormalized `movie`, `cinema`, `theater`, `price`, `start_time`, `type`, `language`, `created_at`, `updated_at` (match [ShowtimeDocMapper](../app/external/billboard/infrastructure/repository/mongo_mappers.py) / `showtimes` collection).

**Semantics:** Upsert Mongo `showtimes` keyed by `showtime_id`.

---

### `showtime.cancelled`

**`event_type`:** `showtime.cancelled`  
**`schema_version`:** `1`

**`payload`:**

| Field | Type | Description |
|-------|------|-------------|
| `showtime_id` | integer | |
| `cancelled_at` | string (ISO 8601) | |

**Semantics:** Delete row or set `cancelled` flag depending on ticket-domain rules.

---

### `movie.metadata.updated` (optional)

**`event_type`:** `movie.metadata.updated`  
**`schema_version`:** `1`

**`payload`:** `movie_id`, title and fields duplicated on showtime documents.

**Semantics:** Only needed if movie titles are denormalized on showtimes and must be refreshed without full showtime snapshot.

---

## Wallet-service events (`wallet.events` topic)

Keep payloads **financial**; do not embed full billboard graphs.

### `payment.authorized`

**`event_type`:** `payment.authorized`  
**`schema_version`:** `1`

**`payload`:**

| Field | Type | Description |
|-------|------|-------------|
| `payment_id` | string | Wallet/payment reference |
| `user_id` | string | Subject |
| `amount` | string (decimal) | Authorized amount |
| `currency` | string | ISO 4217 |
| `metadata` | object | Optional: `order_id`, `showtime_id` references for ticket correlation |

---

### `payment.captured`

**`event_type`:** `payment.captured`  
**`schema_version`:** `1`

**`payload`:** `payment_id`, `captured_at`, optional `metadata` for ticket issuance.

---

### `payment.failed`

**`event_type`:** `payment.failed`  
**`schema_version`:** `1`

**`payload`:** `payment_id`, `reason_code`, `occurred_at`.

---

## Governance

- One **owner** per `event_type` (usually the owning squad).
- **Additive** changes: new optional fields in `payload` with same `schema_version` only if consumers ignore unknown fields.
- **Breaking** changes: bump `schema_version` or add a new `event_type` (e.g. `showtime.upserted.v2`).
