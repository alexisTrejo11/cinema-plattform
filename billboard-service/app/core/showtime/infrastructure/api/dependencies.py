from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db

# REPO
from app.core.showtime.infrastructure.persistence.sqlalchemy import (
    SQLAlchemyShowtimeRepository,
    SQLAlchemyShowtimeSeatRepository,
)

# USECASE
from app.core.showtime.application.use_cases import (
    ScheduleShowtimeUseCase,
    UpdateShowtimeUseCase,
    DeleteShowtimeUseCase,
)
from app.core.showtime.application.use_cases import (
    GetShowtimesUseCase,
    GetShowtimeByIdUseCase,
    ListShowtimeSeatsUseCase,
    GetShowtimeSeatByIdUseCase,
    TakeSeatUseCase,
    CancelSeatUseCase,
)

# THEATER
from app.core.theater.infrastructure.persistence.sqlalchemy import (
    SQLAlchemyTheaterSeatRepository,
    SQLAlchemyTheaterRepository,
)

# DOMAIN SERVICES
from app.core.showtime.domain.services import (
    ShowtimeValidationService,
    ShowTimeSeatService,
)


# COMMAND SHOWTIME
async def schedule_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> ScheduleShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    theater_seat_repository = SQLAlchemyTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(
        showtime_repo, theater_seat_repository
    )
    showtime_seat_service = ShowTimeSeatService(
        theater_seat_repository, showtime_seat_repo
    )

    return ScheduleShowtimeUseCase(
        showtime_repo, validation_service, showtime_seat_service
    )


async def update_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> UpdateShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    theater_seat_repository = SQLAlchemyTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(
        showtime_repo, theater_seat_repository
    )
    return UpdateShowtimeUseCase(showtime_repo, validation_service)


async def delete_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return DeleteShowtimeUseCase(showtime_repo)


# QUERIES SHOWTIME
async def get_showtimes_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetShowtimesUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimesUseCase(showtime_repo)


async def get_showtime_by_id_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetShowtimeByIdUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimeByIdUseCase(showtime_repo)


# SEAT
async def get_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetShowtimeSeatByIdUseCase:
    showtime_seat_repo = SQLAlchemyTheaterSeatRepository(db)
    return GetShowtimeSeatByIdUseCase(showtime_seat_repo)


async def list_showtimes_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListShowtimeSeatsUseCase:
    showtime_seat_repo = SQLAlchemyTheaterSeatRepository(db)
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return ListShowtimeSeatsUseCase(showtime_seat_repo, showtime_repo)


async def take_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> TakeSeatUseCase:
    showtime_seat_repo = SQLAlchemyTheaterSeatRepository(db)
    return TakeSeatUseCase(showtime_seat_repo)


async def cancel_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> CancelSeatUseCase:
    showtime_seat_repo = SQLAlchemyTheaterSeatRepository(db)
    return CancelSeatUseCase(showtime_seat_repo)
