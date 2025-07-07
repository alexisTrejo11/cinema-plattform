# Payment Service API

A FastAPI microservice for managing cinema payments.

## Features

- **Health Check**: `/health` endpoint for service monitoring
- **Ping**: `/ping` endpoint for basic connectivity test
- **Auto Documentation**: Available at `/docs` (Swagger UI) and `/redoc`

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```

The service will be available at `http://localhost:8000`

### Using Docker

1. Build and run with docker-compose:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:8004`

## API Endpoints

- `GET /` - Service information
- `GET /health` - Health check endpoint
- `GET /ping` - Simple ping endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Environment Variables

Configure the following variables in `.env`:

- `DEBUG` - Enable debug mode (default: True)
- `API_VERSION` - API version (default: 1.0.0)
- `APP_PORT` - Application port (default: 8000)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Application secret key
- `JWT_SECRET_KEY` - JWT signing key

## Testing the Service

```bash
# Health check
curl http://localhost:8000/health

# Ping
curl http://localhost:8000/ping

# Service info
curl http://localhost:8000/
```
