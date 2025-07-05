import pytest
from decimal import Decimal
from datetime import datetime
from typing import AsyncGenerator
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.ticket.infrastructure.repository.sql_alch_ticket_repository import SQLAlchemyTicketRepository
from app.ticket.infrastructure.models.ticket_model import TicketModel
from app.ticket.domain.entities.ticket import Ticket, CustomerDetails, TicketStatus, TicketType, PaymentDetails, PriceDetails

from app.seats.infra.model import ShowtimeSeatModel
from app.seats.infra.sql_alch_repository import SqlAlchemySeatRepository
from app.seats.domain.showtime_seat import ShowtimeSeat

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def setup_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(TicketModel.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(TicketModel.metadata.drop_all)

@pytest.fixture
async def async_session(async_engine, setup_db) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            # Clean up all data after the test
            try:
                # Check if session is in a bad state and rollback if needed
                if session.in_transaction() and session.get_transaction().is_active:
                    await session.rollback()
                
                # Clean up data
                await session.execute(text("DELETE FROM showtime_seats"))
                await session.execute(text("DELETE FROM tickets"))
                await session.commit()
            except Exception:
                # If cleanup fails, just rollback
                await session.rollback()

@pytest.fixture
def ticket_repository(async_session):
    return SQLAlchemyTicketRepository(async_session)


# Ticket
@pytest.fixture
async def sample_ticket_model(async_session):
    ticket = TicketModel(
        movie_id=1,
        showtime_id=1,
        user_id=1,
        customer_email="test@example.com",
        price=10.50,
        price_currency="USD",
        status=TicketStatus.RESERVED.value,
        ticket_type=TicketType.DIGITAL.value,
    )
    async_session.add(ticket)
    await async_session.commit()
    await async_session.refresh(ticket)
    return ticket

@pytest.fixture
def sample_ticket_entity():
    price_details = PriceDetails(Decimal("10.50"), "USD")
    customer_details = CustomerDetails("modelcustomer_email@mail.com", 1, "0.0.0.0")
    return Ticket(
        id=None,
        movie_id=2,
        showtime_id=2,
        price_details=price_details,
        customer_details=customer_details,
        status=TicketStatus.RESERVED,
        ticket_type=TicketType.DIGITAL,
    )
    
    

# Seats
@pytest.fixture
async def sample_seat_model(async_session):
    seat = ShowtimeSeatModel(
        showtime_id=1,
        seat_id=101,
        seat_name="A1",
        is_available=True,
        created_at=datetime.now(),
    )
    async_session.add(seat)
    await async_session.commit()
    await async_session.refresh(seat)
    return seat

@pytest.fixture
async def multiple_seat_models(async_session):
    seats = [
        ShowtimeSeatModel(
            id=1 + i,
            showtime_id=1,
            seat_id=101 + i,
            seat_name=f"A{i+1}",
            is_available=True,
            created_at=datetime.now(),
        ) for i in range(5)
    ]
    async_session.add_all(seats)
    await async_session.commit()
    for seat in seats:
        await async_session.refresh(seat)
    return seats

@pytest.fixture
def sample_seat_entity():
    return ShowtimeSeat(
        showtime_id=2,
        seat_id=201,
        seat_name="B1",
        is_available=False,
        ticket_id=1,
        id=None
    )
    

@pytest.fixture
def seat_repository(async_session):
    return SqlAlchemySeatRepository(async_session)