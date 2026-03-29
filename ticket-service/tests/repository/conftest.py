import asyncio
from datetime import datetime
from decimal import Decimal
from typing import AsyncGenerator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.internal.seats.domain.showtime_seat import ShowtimeSeat
from app.internal.seats.infra.model import ShowtimeSeatModel
from app.internal.seats.infra.sql_alch_repository import SqlAlchemySeatRepository
from app.internal.ticket.domain.entities.ticket import Ticket
from app.internal.ticket.domain.valueobjects.enums import TicketStatus, TicketType
from app.internal.ticket.domain.valueobjects.helping_classes import (
    CustomerDetails,
    PaymentDetails,
    PriceDetails,
)
from app.internal.ticket.infrastructure.models.ticket_model import TicketModel
from app.internal.ticket.infrastructure.repository.sql_alch_ticket_repository import (
    SQLAlchemyTicketRepository,
)


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
            try:
                if session.in_transaction() and session.get_transaction().is_active:
                    await session.rollback()

                await session.execute(text("DELETE FROM showtime_seats"))
                await session.execute(text("DELETE FROM tickets"))
                await session.commit()
            except Exception:
                await session.rollback()


@pytest.fixture
def ticket_repository(async_session):
    return SQLAlchemyTicketRepository(async_session)


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
    price_details = PriceDetails(price=Decimal("10.50"), currency="USD")
    customer_details = CustomerDetails(
        user_email="modelcustomer_email@mail.com",
        id=1,
        customer_ip_address="0.0.0.0",
    )
    payment_details = PaymentDetails(
        id=1,
        transaction_id=123,
        type="digital",
        method="card",
        currency="USD",
    )
    return Ticket(
        id=0,
        movie_id=2,
        showtime_id=2,
        price_details=price_details,
        payment_details=payment_details,
        customer_details=customer_details,
        status=TicketStatus.RESERVED,
        ticket_type=TicketType.DIGITAL,
    )


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
        )
        for i in range(5)
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
        id=None,
    )


@pytest.fixture
def seat_repository(async_session):
    return SqlAlchemySeatRepository(async_session)
