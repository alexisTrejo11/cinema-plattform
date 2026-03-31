# Ticket-service: consumer mapping and idempotency

How inbound Kafka events update the **local read replica** in MongoDB and how duplicate or out-of-order messages are handled.

## Mongo collections (read models)

Repositories under `app/external/billboard/infrastructure/repository/` use:

| Collection | Primary key field(s) in queries | Repository |
|------------|----------------------------------|------------|
| `cinemas` | `cinema_id` | `MongoCinemaRepository` |
| `theaters` | `theater_id` | `MongoTheaterRepository` |
| `showtimes` | `showtime_id` | `MongoShowtimeRepository` |

Documents are built with mappers in [`mongo_mappers.py`](../app/external/billboard/infrastructure/repository/mongo_mappers.py). Event payloads should carry enough data to populate the same document shape (or a superset pruned in the consumer).

**Note:** Some legacy field typos exist in code (`theathers` vs `theaters`, `theather_id` in a few queries). New consumer implementations should align with **canonical** keys (`showtime_id`, `theater_id`) and follow-up refactors can fix repository inconsistencies.

---

## Event → collection mapping

| `event_type` | Action | Target | Handler summary |
|--------------|--------|--------|-------------------|
| `cinema.upserted` | upsert | `cinemas` | `replace_one` / `update_one` with `cinema_id` filter |
| `cinema.deactivated` | update or delete | `cinemas` | Set `is_active: false` or delete per policy |
| `theater.upserted` | upsert | `theaters` | Full document for `theater_id`; update embedded lists in `cinemas` if projection nests theaters |
| `theater.deleted` | delete | `theaters` | `delete_one({ theater_id })`; remove from parent cinema if embedded |
| `showtime.upserted` | upsert | `showtimes` | Ensure document includes `showtime_id` for indexing |
| `showtime.cancelled` | delete or flag | `showtimes` | Prefer soft-delete if tickets still reference the row |
| `movie.metadata.updated` | partial update | `showtimes` | Denormalized title patches where `movie_id` matches |

Wallet events do not necessarily write to billboard collections; they feed **ticket issuance / payment state** (PostgreSQL or other stores)—define in ticket domain module when implementing handlers.

---

## Idempotency

**Problem:** Kafka provides at-least-once delivery; the same `event_id` may be processed twice.

**Strategies (pick one or combine):**

1. **Processed-event log (recommended for ticket-service)**  
   - Collection `kafka_processed_events` with unique index on `event_id`.  
   - Before applying business logic, `insert` event_id; on duplicate key, skip (no-op success).

2. **Natural key + monotonic version**  
   - Store `source_version` or `updated_at` on each document; apply update only if incoming `occurred_at` or version is **newer** than stored.

3. **Upsert by id**  
   - For pure snapshots (`showtime.upserted`), replacing the full document by `showtime_id` is naturally idempotent.

Use **(1)** for correctness across all event types; use **(2)** as defense-in-depth for ordering.

---

## Ordering and late events

- **Theater before showtime:** If a showtime arrives before its theater row exists, either retry with backoff, or buffer in memory (complex). Prefer billboard-service to publish **theater.upserted** before dependent showtimes, or use partition keys that serialize related work (not always possible). Document: consumer may **defer** processing with a short delay queue.

- **Cinema embedding:** If `cinemas` embed `theaters`, a `theater.upserted` event may require updating both `theaters` and the parent `cinemas` document.

---

## Consumer groups and configuration

- **Group:** `ticket-service-billboard` for `billboard.events`; `ticket-service-wallet` for `wallet.events`.
- **Env vars:** See `KAFKA_CONSUMER_*` in [`app_config.py`](../app/config/app_config.py).

---

## Observability

- Log `event_id`, `event_type`, `correlation_id`, processing duration.
- Metrics: consumer lag, handler errors, DLQ publish rate.
- Alerts on lag above SLO (e.g. > 5 minutes sustained).
