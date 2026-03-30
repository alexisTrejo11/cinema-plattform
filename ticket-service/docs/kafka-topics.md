# Kafka topics, partitioning, retention, and DLQ

Operational contract for the cinema platform event bus. Environment-specific cluster URLs live in deployment config; this document names **topics** and **policies**.

## Topic inventory

| Topic name | Producers | Primary consumers | Purpose |
|------------|-----------|-----------------|----------|
| `billboard.events` | billboard-service | ticket-service (`ticket-service-billboard` group), others TBD | Cinema, theater, showtime (and optional movie) domain events |
| `wallet.events` | wallet-service | ticket-service (`ticket-service-wallet` group), others TBD | Payment lifecycle events |
| `billboard.events.dlq` | (Kafka streams / manual replay) | ops, ticket-service replay job | Dead letters for failed `billboard.events` processing |
| `wallet.events.dlq` | same | same | Dead letters for `wallet.events` |

**Naming convention:** `{domain}.events` for primary streams; `{domain}.events.dlq` for poison messages after retry exhaustion.

Alternative for very high volume: split billboard into `billboard.cinema.events`, `billboard.showtime.events`, etc. Start with a **single** `billboard.events` unless ordering or retention requirements force a split.

---

## Partition keys

Ordering is guaranteed **per partition** only. Use a key derived from the aggregate id:

| Event family | Suggested Kafka record key | Rationale |
|--------------|---------------------------|-----------|
| Cinema | `cinema:{cinema_id}` | Serialize updates per cinema |
| Theater | `theater:{theater_id}` | Seat layout changes ordered per theater |
| Showtime | `showtime:{showtime_id}` | Start time / cancellation ordered per showtime |
| Movie (optional) | `movie:{movie_id}` | Independent of cinema |
| Wallet | `user:{user_id}` or `payment:{payment_id}` | Use `payment_id` if strict payment ordering; `user_id` if balancing load is priority |

Producers must set the key consistently so ticket-service consumers see ordered updates for the same entity.

---

## Retention

| Topic | Recommended minimum retention | Notes |
|-------|------------------------------|--------|
| `billboard.events` | 7 days (dev), 14–30 days (prod) | Increase if reprocessing or new consumers need history |
| `wallet.events` | 30–90 days | May be subject to finance/compliance; align with legal |
| `*.dlq` | 90 days or indefinite | Until incidents are resolved and messages replayed or dropped |

Tune `retention.ms` and `retention.bytes` per cluster capacity.

---

## Consumer groups (ticket-service)

| Group id | Subscribes | Instance scaling |
|----------|------------|------------------|
| `ticket-service-billboard` | `billboard.events` | Horizontal; partitions split work |
| `ticket-service-wallet` | `wallet.events` | Same |

Do **not** share one group for both topics unless using a single processor binary that multiplexes (still two subscriptions are clearer as separate groups in most frameworks).

---

## DLQ policy

1. On handler failure after **N** retries (e.g. 3–5 with exponential backoff), publish the original record (headers + value) to the matching `.dlq` topic with extra headers: `failure_reason`, `failed_at`, `consumer_group`.
2. Main topic offset is committed only for **successfully** processed messages (at-least-once delivery).
3. Replay: dedicated tool or consumer that reads `.dlq`, fixes data or code, and optionally republishes to the main topic with a new `event_id`.

---

## Security

- TLS to brokers in non-dev environments.
- SASL/SCRAM or mTLS as required by platform.
- No PAN, CVV, or raw card data in payloads.

---

## Alignment with application settings

Default topic and group names are mirrored in [`app/config/app_config.py`](../app/config/app_config.py) for ticket-service (see `KAFKA_TOPIC_*`, `KAFKA_CONSUMER_GROUP_*`).
