# Ticket-service Docker stack

## Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Postgres, Redis, **MongoDB**, app replicas, gRPC, nginx |
| `docker-compose.kafka-bridge.example.yml` | Optional merge file to join [Kafka infra](../kafka-infra/) (`kafka_infra_shared`) |
| `dockerfile` | Multi-stage image for the Python app |
| `docker-entrypoint.sh` | Migrations + `serve` / `serve-grpc` |

## Run

From `ticket-service/docker`:

```bash
docker compose up -d --build
```

- **Postgres**: host port `5431` → container `5432`
- **Redis**: host `6378` → `6379`
- **MongoDB**: host `27017` → `27017` (override with `MONGO_PORT`)

App containers receive `MONGO_URI=mongodb://mongo:27017` and `MONGO_DB_NAME` (default `cinema_tickets`), overriding a host-only `.env` that points Mongo at `localhost`.

## Kafka (separate compose)

Kafka is **not** bundled here. Use [`../kafka-infra/`](../kafka-infra/) as a standalone stack, then attach this project with the example overlay:

```bash
cd ../kafka-infra && docker compose up -d
cd ../docker
docker compose -f docker-compose.yml -f docker-compose.kafka-bridge.example.yml up -d
```

Bootstrap from inside Docker: `kafka:9092`. From your laptop (kafka-infra only): `localhost:9094`.
