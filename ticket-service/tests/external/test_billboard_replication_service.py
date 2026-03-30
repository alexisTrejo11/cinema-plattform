"""Unit tests for Kafka-driven billboard read-model sync."""

from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.external.billboard.application.services.billboard_replication_service import (
    BillboardReplicationService,
)
from app.external.billboard.core.enums.showtime_enum import ShowtimeLanguage, ShowtimeType
from app.external.billboard.core.enums.theather_enum import TheaterType
from app.external.billboard.core.entities.cinema import Cinema
from app.external.billboard.core.entities.movie import Movie
from app.external.billboard.core.entities.showtime import Showtime
from app.external.billboard.core.entities.theater import Theater


@pytest.fixture
def theater_payload() -> dict:
    return {
        "theater_id": 1,
        "cinema_id": 10,
        "name": "Hall A",
        "capacity": 100,
        "theater_type": "STANDARD",
        "seats": [
            {
                "seat_id": 1,
                "theater_id": 1,
                "seat_row": "A",
                "seat_number": 1,
                "seat_type": "STANDARD",
                "is_active": True,
            }
        ],
        "is_active": True,
        "maintenance_mode": False,
    }


@pytest.mark.asyncio
async def test_theater_upserted_calls_save(theater_payload: dict) -> None:
    cinema_repo = AsyncMock()
    theater_repo = AsyncMock()
    showtime_repo = AsyncMock()
    dedup = AsyncMock()
    dedup.try_claim = AsyncMock(return_value=True)
    dedup.release = AsyncMock()

    svc = BillboardReplicationService(cinema_repo, theater_repo, showtime_repo, dedup)
    await svc.apply_envelope(
        {
            "event_id": "evt-1",
            "event_type": "theater.upserted",
            "payload": theater_payload,
        }
    )

    theater_repo.save.assert_awaited_once()
    saved = theater_repo.save.call_args[0][0]
    assert isinstance(saved, Theater)
    assert saved.theater_id == 1


@pytest.mark.asyncio
async def test_duplicate_event_id_skips_processing(theater_payload: dict) -> None:
    cinema_repo = AsyncMock()
    theater_repo = AsyncMock()
    showtime_repo = AsyncMock()
    dedup = AsyncMock()
    dedup.try_claim = AsyncMock(return_value=False)

    svc = BillboardReplicationService(cinema_repo, theater_repo, showtime_repo, dedup)
    await svc.apply_envelope(
        {
            "event_id": "evt-dup",
            "event_type": "theater.upserted",
            "payload": theater_payload,
        }
    )

    theater_repo.save.assert_not_called()


def _minimal_showtime_payload() -> dict:
    movie = Movie(
        id=1,
        title="Test",
        minute_duration=120,
        release_date=date(2024, 1, 1),
        end_date=date(2025, 1, 1),
    )
    cinema = Cinema(
        cinema_id=10,
        name="Cine",
        address="123 Street",
        theaters=[],
    )
    theater = Theater(
        theater_id=1,
        cinema_id=10,
        name="H1",
        capacity=50,
        theater_type=TheaterType.STANDARD,
        seats=[],
    )
    st = Showtime(
        id=99,
        movie=movie,
        cinema=cinema,
        theater=theater,
        price=Decimal("10.00"),
        start_time=datetime(2025, 6, 1, 20, 0, 0),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.DUBBED_SPANISH,
    )
    d = st.model_dump(mode="json")
    d["showtime_id"] = 99
    return d


@pytest.mark.asyncio
async def test_showtime_upserted_creates_when_missing() -> None:
    cinema_repo = AsyncMock()
    theater_repo = AsyncMock()
    showtime_repo = AsyncMock()
    showtime_repo.get_by_id = AsyncMock(return_value=None)
    dedup = AsyncMock()
    dedup.try_claim = AsyncMock(return_value=True)
    dedup.release = AsyncMock()

    svc = BillboardReplicationService(cinema_repo, theater_repo, showtime_repo, dedup)
    await svc.apply_envelope(
        {
            "event_id": "evt-st-1",
            "event_type": "showtime.upserted",
            "payload": _minimal_showtime_payload(),
        }
    )

    showtime_repo.create.assert_awaited_once()
    showtime_repo.update.assert_not_called()
