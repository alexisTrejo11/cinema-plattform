# Producer rollout and migration roadmap

Recommended order to introduce Kafka-backed replication without blocking ticket-service development.

## Phase 0 — Contracts frozen in docs

- Finalize [event-catalog.md](./event-catalog.md) and [kafka-topics.md](./kafka-topics.md) with owning teams.
- Optionally publish JSON Schema or AsyncAPI fragments in a shared repo for CI validation.

## Phase 1 — Kafka cluster and topics

- Provision topics: `billboard.events`, `wallet.events`, matching DLQs.
- Configure retention, partitions (estimate QPS × retention for sizing), ACLs.
- Smoke-test produce/consume from a throwaway CLI.

## Phase 2 — Billboard-service producers (source of truth)

1. Add outbox or **transactional** emit after DB commit (recommended pattern to avoid lost/cross events).
2. Implement emitters for: `theater.upserted`, `showtime.upserted`, `showtime.cancelled`, then `cinema.*` as needed.
3. Deploy to staging; verify messages on `billboard.events` with correct keys.

## Phase 3 — Ticket-service Mongo backfill

- **One-time** job: export current billboard data via REST or DB snapshot into ticket-service Mongo (`cinemas`, `theaters`, `showtimes`) using existing mappers.
- Validate row counts and spot-check against billboard-service API.

## Phase 4 — Ticket-service consumers

- Implement consumer group `ticket-service-billboard` reading `billboard.events` from **`latest`** if backfill is complete, or **`earliest`** if you need to replay from topic start.
- Wire idempotency ([ticket-service-consumer-spec.md](./ticket-service-consumer-spec.md)).
- Enable in production with monitoring; optional **dual-read** period comparing API vs Mongo.

## Phase 5 — Wallet-service producers

- Emit `payment.*` events to `wallet.events` when payment state changes.
- Ticket-service: add `ticket-service-wallet` consumer and domain handlers (ticket creation, failure paths).

## Phase 6 — Decommission synchronous paths

- Reduce or remove hot-path HTTP calls from ticket-service to billboard-service for read-only data once lag and error budgets are green.

---

## Rollback

- Disable consumers via `KAFKA_CONSUMER_ENABLED=false` (ticket-service); fall back to REST/sync loading documented in runbooks.
- Producers can be feature-flagged per event type in billboard-service without stopping reads.

---

## Checklist before production cutover

- [ ] Event catalog signed off by billboard + ticket owners  
- [ ] DLQ runbook and on-call know how to replay  
- [ ] Pager thresholds for consumer lag  
- [ ] Backfill job idempotent and rerunnable  
