from tests.conftest import *
from typing import Dict, Any
from app.core.theater.domain.theater import Theater, TheaterType
from app.core.theater.domain.seat import TheaterSeat, SeatType
from app.core.theater.infrastructure.persistence.sqlalch_theater_repository import (
    SQLAlchemyTheaterRepository as TheaterRepository,
)
from app.core.theater.infrastructure.persistence.sqlalch_seats_repository import (
    SqlAlchemyTheaterSeatRepository as TheaterSeatRepository,
)


@pytest.fixture
def sample_theater() -> Theater:
    return Theater(
        name="Main Theater",
        capacity=200,
        theater_type=TheaterType.VIP,
        is_active=True,
        maintenance_mode=False,
        cinema_id=1,
    )


@pytest.fixture
def updated_theater_data() -> Dict[str, Any]:
    return {
        "name": "Updated Theater Name",
        "capacity": 150,
        "theater_type": TheaterType.IMAX,
        "is_active": False,
        "maintenance_mode": True,
    }


@pytest_asyncio.fixture(scope="function")
async def theater_repo(session: AsyncSession) -> TheaterRepository:
    return TheaterRepository(session)


@pytest.fixture
def sample_seat() -> TheaterSeat:
    return TheaterSeat(
        id=None,
        theater_id=1,
        seat_row="A",
        seat_number=1,
        seat_type=SeatType.STANDARD,
        is_active=True,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def updated_seat_data() -> Dict[str, Any]:
    return {
        "seat_row": "B",
        "seat_number": 2,
        "seat_type": SeatType.VIP,
        "is_active": False,
    }


@pytest_asyncio.fixture(scope="function")
async def seat_repo(session: AsyncSession) -> TheaterSeatRepository:
    return TheaterSeatRepository(session)
