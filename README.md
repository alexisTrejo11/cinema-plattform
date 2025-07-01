# Cinema Ticket Service

A robust FastAPI microservice for managing cinema ticket operations using Clean Architecture principles.

## Features

- **Clean Architecture**: Separated layers with dependency inversion
- **Domain-Driven Design**: Pure business logic in domain entities
- **Dependency Injection**: Using dependency-injector container
- **SQLAlchemy ORM**: Robust database operations
- **Comprehensive DTOs**: Proper data validation with Pydantic
- **Business Logic**: Ticket confirmation, cancellation, refunds
- **Seat Management**: Prevent double booking
- **Multiple Seat Types**: Standard, VIP, Premium with different pricing

## Architecture

```
app/
├──ticket/
    ├── domain/
    │   ├── entities/          # Pure business logic
    │   └── value_objects/     # Helping Classes for Tickets
    ├── application/
    │   ├── dtos/             # Data transfer objects
    │   └── use_cases/        # Application business rules
    │   └── repositories/     # Abstract interfaces
    ├── infrastructure/
    │   ├── models/           # SQLAlchemy models
    │   ├── repositories/     # Repository implementations
    │   └── container.py      # DI container
    └── presentation/
        └── controllers/      # FastAPI controllers
```

## API Endpoints

- `POST /api/v1/tickets/` - Create ticket reservation
- `GET /api/v1/tickets/{ticket_id}` - Get ticket by ID
- `GET /api/v1/tickets/user/{user_id}` - Get user tickets
- `GET /api/v1/tickets/showtime/{showtime_id}` - Get showtime tickets
- `PUT /api/v1/tickets/{ticket_id}` - Update ticket
- `PATCH /api/v1/tickets/{ticket_id}/confirm` - Confirm ticket
- `PATCH /api/v1/tickets/{ticket_id}/cancel` - Cancel ticket
- `PATCH /api/v1/tickets/{ticket_id}/use` - Use ticket
- `POST /api/v1/tickets/{ticket_id}/refund` - Process refund

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up PostgreSQL database
3. Update DATABASE_URL in environment
4. Run SQL queries: `pqsl....`
5. Start server: `python -m app.main`

## Docker

```bash
docker-compose up -d
```

The service will be available at http://localhost:8003

## Business Rules

- Tickets start as RESERVED status
- Only reserved tickets can be confirmed
- Refunds allowed up to 2 hours before showtime
- Different processing fees by seat type
- Seat availability checking prevents double booking