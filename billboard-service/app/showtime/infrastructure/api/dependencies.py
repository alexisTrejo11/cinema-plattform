from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db

# REPO
from app.showtime.infrastructure.persistence.sqlalch_show_repository import SQLAlchemyShowtimeRepository
from app.showtime.infrastructure.persistence.sqlalch_show_seat_repository import SqlAlchShowtimeSeatRepository

# SERVICE
from app.showtime.application.service.showtime_validator_service import ShowtimeValidationService
from app.showtime.application.service.showtime_seat_service import ShowTimeSeatService

# USECASE
from app.showtime.application.use_cases.showtime_command_use_cases import ScheduleShowtimeUseCase, UpdateShowtimeUseCase, DeleteShowtimeUseCase
from app.showtime.application.use_cases.showtime_query_use_cases import  GetShowtimesUseCase, GetShowtimeByIdUseCase
from app.showtime.application.use_cases.showtime_seats_use_case import GetShowtimeSeatByIdUseCase, ListShowtimeSeatsUseCase, TakeSeatUseCase, CancelSeatUseCase

# THEATER
from app.theater.infrastructure.persistence.sqlalch_seats_repository import SqlAlchemistTheaterSeatRepository

# COMMAND SHOWTIME
async def schedule_showtime_use_case(db: AsyncSession = Depends(get_db)) -> ScheduleShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    theater_seat_repository = SqlAlchemistTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(showtime_repo, theater_seat_repository)
    showtime_seat_service = ShowTimeSeatService(theater_seat_repository, showtime_seat_repo)

    return ScheduleShowtimeUseCase(showtime_repo, validation_service, showtime_seat_service)

async def update_showtime_use_case(db: AsyncSession = Depends(get_db)) -> UpdateShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    theater_seat_repository = SqlAlchemistTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(showtime_repo, theater_seat_repository)
    return UpdateShowtimeUseCase(showtime_repo, validation_service)

async def delete_showtime_use_case(db: AsyncSession = Depends(get_db)) -> DeleteShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return DeleteShowtimeUseCase(showtime_repo)


# QUERIES SHOWTIME
async def get_showtimes_use_case(db: AsyncSession = Depends(get_db)) -> GetShowtimesUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimesUseCase(showtime_repo)

async def get_showtime_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetShowtimeByIdUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimeByIdUseCase(showtime_repo)


# SEAT
async def get_showtime_seat_use_case(db: AsyncSession = Depends(get_db)) -> GetShowtimeSeatByIdUseCase:
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    return GetShowtimeSeatByIdUseCase(showtime_seat_repo)

async def list_showtimes_seat_use_case(db: AsyncSession = Depends(get_db)) -> ListShowtimeSeatsUseCase:
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return ListShowtimeSeatsUseCase(showtime_seat_repo, showtime_repo)

async def take_showtime_seat_use_case(db: AsyncSession = Depends(get_db)) -> TakeSeatUseCase:
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    return TakeSeatUseCase(showtime_seat_repo)

async def cancel_showtime_seat_use_case(db: AsyncSession = Depends(get_db)) -> CancelSeatUseCase:
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    return CancelSeatUseCase(showtime_seat_repo)
