# catalog-service

Catalog service that owns cinema, theater, and movie concerns.

## What it exposes

- HTTP APIs for:
  - cinemas
  - movies
  - theaters / theater seats
- gRPC API (generic unary methods) used by billboard service:
  - `IsMovieActive`
  - `IsCinemaActive`
  - `TheaterHasSeats`
  - `ListTheaterSeats`

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Environment

Uses local settings in `catalog-service/app/config/app_config.py`.
Make sure:

- `API_PORT` is unique for catalog HTTP API
- `GRPC_PORT` is set to catalog gRPC port (default `50056` recommended)
- billboard service points `GRPC_CATALOG_TARGET` to `catalog-service` (`host:port`)
