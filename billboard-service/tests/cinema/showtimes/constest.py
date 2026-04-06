from tests.conftest import *

import pytest
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from  app.showtime.domain.entities.showtime import Showtime, Seats, Decimal
from  app.showtime.domain.enums import *
from  app.showtime.infrastructure.persistence.sqlalch_show_repository import (
    SQLAlchemyShowtimeRepository as ShowtimeRepository,
)


@pytest_asyncio.fixture(scope="function")
async def showtime_repo(session: AsyncSession) -> ShowtimeRepository:
    """Fixture para proporcionar una instancia del repositorio de Showtimes."""
    return ShowtimeRepository(session)


@pytest.fixture
def create_seats():
    """
    Fixture factory to create a list of Seats objects.
    Returns a function that takes num_seats and optionally taken_seats_count.
    """

    def _create_seats(num_seats: int, taken_seats_count: int = 0) -> List[Seats]:
        seats = []
        for i in range(num_seats):
            row = chr(65 + (i // 10))  # A, B, C...
            number = (i % 10) + 1
            is_taken = True if i < taken_seats_count else False
            seats.app.d(
                Seats(
                    seat_id=i + 1, seat_row=row, seat_number=number, is_taken=is_taken
                )
            )
        return seats

    return _create_seats


@pytest.fixture
def sample_showtime(create_seats) -> Showtime:
    """
    Fixture para un objeto Showtime de ejemplo válido y futuro.
    Tiene seats y available_seats configurados.
    """
    total_seats = 100
    available_seats = 90
    seats_list = create_seats(
        total_seats, total_seats - available_seats
    )  # 10 asientos tomados

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        hours=2
    )
    end_time_utc = start_time_utc + timedelta(minutes=150)  # 2 horas y 30 minutos

    return Showtime(
        id=None,
        movie_id=1,
        cinema_id=10,
        theater_id=101,
        price=Decimal("12.50"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def old_showtime(create_seats) -> Showtime:
    """
    Fixture para un objeto Showtime que ya ha pasado.
    Útil para probar filtros de "incoming" o validaciones de fechas.
    """
    total_seats = 80
    available_seats = 80  # Asume que no se tomaron asientos para un showtime pasado
    seats_list = create_seats(total_seats, 0)

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(
        days=5, hours=3
    )
    end_time_utc = start_time_utc + timedelta(minutes=90)  # 1 hora y 30 minutos

    return Showtime(
        id=None,
        movie_id=2,
        cinema_id=10,
        theater_id=102,
        price=Decimal("8.00"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def future_showtime_different_cinema(create_seats) -> Showtime:
    """
    Fixture para un Showtime futuro en un cine diferente.
    """
    total_seats = 120
    available_seats = 110
    seats_list = create_seats(total_seats, total_seats - available_seats)

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        days=1, hours=5
    )
    end_time_utc = start_time_utc + timedelta(minutes=180)  # 3 horas

    return Showtime(
        id=None,
        movie_id=3,
        cinema_id=20,  # Diferente cinema_id
        theater_id=201,
        price=Decimal("15.00"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_3D,
        language=ShowtimeLanguage.ORIGINAL_SPANISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def future_showtime_different_movie(create_seats) -> Showtime:
    """
    Fixture para un Showtime futuro de una película diferente pero en el mismo cine.
    """
    total_seats = 90
    available_seats = 85
    seats_list = create_seats(total_seats, total_seats - available_seats)

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        hours=4
    )
    end_time_utc = start_time_utc + timedelta(minutes=110)

    return Showtime(
        id=None,
        movie_id=99,  # Diferente movie_id
        cinema_id=10,  # Mismo cinema_id que sample_showtime
        theater_id=103,
        price=Decimal("10.00"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def showtime_with_no_available_seats(create_seats) -> Showtime:
    """
    Fixture para un Showtime futuro sin asientos disponibles.
    """
    total_seats = 50
    available_seats = 0
    seats_list = create_seats(total_seats, total_seats)  # Todos los asientos tomados

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        hours=24
    )
    end_time_utc = start_time_utc + timedelta(minutes=120)

    return Showtime(
        id=None,
        movie_id=4,
        cinema_id=10,
        theater_id=104,
        price=Decimal("9.50"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def showtime_invalid_price(create_seats) -> Showtime:
    """
    Fixture para un Showtime con un precio inválido (fuera de rango).
    """
    total_seats = 100
    available_seats = 100
    seats_list = create_seats(total_seats, 0)

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        hours=2
    )
    end_time_utc = start_time_utc + timedelta(minutes=120)

    return Showtime(
        id=None,
        movie_id=5,
        cinema_id=10,
        theater_id=105,
        price=Decimal("2.00"),  # Precio inválido
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def showtime_too_far_in_future(create_seats) -> Showtime:
    """
    Fixture para un Showtime programado demasiado lejos en el futuro.
    """
    total_seats = 100
    available_seats = 100
    seats_list = create_seats(total_seats, 0)

    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        days=35
    )  # Más de 30 días
    end_time_utc = start_time_utc + timedelta(minutes=120)

    return Showtime(
        id=None,
        movie_id=6,
        cinema_id=10,
        theater_id=106,
        price=Decimal("12.00"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def showtime_overlapp.g_with_another(create_seats) -> Showtime:
    """
    Fixture para un Showtime que se superpone con otro.
    Requiere que se genere otro showtime para la superposición.
    """
    total_seats = 70
    available_seats = 70
    seats_list = create_seats(total_seats, 0)

    # Este showtime se superpondrá con 'sample_showtime' si tienen el mismo theater_id
    # ajusta el theater_id según el test que uses
    start_time_utc = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
        hours=2, minutes=30
    )
    end_time_utc = start_time_utc + timedelta(
        minutes=90
    )  # Termina antes que sample_showtime

    return Showtime(
        id=None,
        movie_id=7,
        cinema_id=10,
        theater_id=101,
        price=Decimal("11.00"),
        start_time=start_time_utc,
        end_time=end_time_utc,
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_ENGLISH,
        total_seats=total_seats,
        available_seats=available_seats,
        seats=seats_list,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def showtime_for_update() -> Dict[str, Any]:
    """Fixture para datos de actualización de Showtime."""
    return {
        "price": 12.5,
        "type": ShowtimeType.IMAX_3D,
        "language": ShowtimeLanguage.DUBBED_ENGLISH,
    }
