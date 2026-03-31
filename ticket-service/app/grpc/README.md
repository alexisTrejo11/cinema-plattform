# gRPC in ticket-service

## Layout

| Path | Role |
|------|------|
| [`protos/`](protos/) | `.proto` sources (`cinema.payment.v1`, `cinema.billboard.v1`, `cinema.ticket.v1`) |
| [`generated/`](generated/) | **Generated** `_pb2.py` / `_pb2_grpc.py` (do not edit; regenerate with script) |
| [`__init__.py`](__init__.py) | Prepends `generated/` to `sys.path` so imports like `payment.v1` resolve |
| [`server.py`](server.py) | Inbound **TicketService.Ping** (minimal; used by `serve-grpc` in Docker) |

Outbound **clients** implementing domain ports live under
[`app/ticket/infrastructure/grpc/`](../ticket/infrastructure/grpc/):

- **Payment** → `cinema.payment.v1.PaymentService` (AuthorizePayment, RefundPayment)
- **Billboard** → `cinema.billboard.v1.SeatAvailabilityService` (AssertSeatsAvailable)

## Regenerate stubs

Requires `grpcio-tools` (see `requirements.txt`):

```bash
chmod +x scripts/generate_grpc.sh
./scripts/generate_grpc.sh
```

## Configuration

Environment variables (see `app/config/app_config.py`):

| Variable | Meaning |
|----------|---------|
| `GRPC_PORT` | Port for **this** process’s gRPC server (default `50055`) |
| `GRPC_PAYMENT_TARGET` | `host:port` for payment service; **empty** = skip payment gRPC |
| `GRPC_BILLBOARD_TARGET` | `host:port` for billboard service; **empty** = skip seat assertion |
| `GRPC_TIMEOUT_SECONDS` | Per-RPC deadline (default `10`) |

## Contracts

Payment and billboard services must implement the RPCs and messages defined in the protos.
If your remote services use different method names, add a thin translation layer or fork the protos
to match those teams’ contracts, then regenerate.
