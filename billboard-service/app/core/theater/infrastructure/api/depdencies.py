from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from app.core.cinema.infrastructure.persistence.sqlalchemy import (
    SQLAlchemyCinemaRepository,
)
from app.core.theater.application.theather_use_cases import (
    GetTheaterByIdUseCase,
    GetTheatersByCinemaUseCase,
    ListTheatersUseCase,
    CreateTheaterUseCase,
    UpdateTheaterUseCase,
    DeleteTheaterUseCase,
)
from app.core.theater.application.seats_use_cases import (
    GetTheaterSeatByIdUseCase,
    GetSeatsByTheaterUseCase,
    CreateTheaterSeatUseCase,
    UpdateTheaterSeatUseCase,
    DeleteTheaterSeatUseCase,
)
from app.core.theater.domain.services import SeatValidationService
from ..persistence.sqlalchemy import (
    SQLAlchemyTheaterRepository,
    SQLAlchemyTheaterSeatRepository,
)


async def get_theater_by_id_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetTheaterByIdUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return GetTheaterByIdUseCase(repo)


async def get_theaters_by_cinema_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetTheatersByCinemaUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return GetTheatersByCinemaUseCase(repo)


async def list_theaters_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListTheatersUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return ListTheatersUseCase(repo)


async def create_theater_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateTheaterUseCase:
    theater_repo = SQLAlchemyTheaterRepository(db)
    cinema_repo = SQLAlchemyCinemaRepository(db)
    return CreateTheaterUseCase(theater_repo, cinema_repo)


async def update_theater_use_case(
    db: AsyncSession = Depends(get_db),
) -> UpdateTheaterUseCase:
    theater_repo = SQLAlchemyTheaterRepository(db)
    cinema_repo = SQLAlchemyCinemaRepository(db)
    return UpdateTheaterUseCase(theater_repo, cinema_repo)


async def delete_theater_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteTheaterUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return DeleteTheaterUseCase(repo)


async def get_theater_seat_by_id_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetTheaterSeatByIdUseCase:
    """
    Dependency for GetTheaterSeatByIdUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SQLAlchemyTheaterSeatRepository(db)

    return GetTheaterSeatByIdUseCase(repository)


async def get_seats_by_theater_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetSeatsByTheaterUseCase:
    """
    Dependency for GetSeatsByTheaterUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SQLAlchemyTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)

    return GetSeatsByTheaterUseCase(
        seat_repository=seat_repository, theater_repository=theather_repository
    )


async def create_theater_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateTheaterSeatUseCase:
    """
    Dependency for SaveTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SQLAlchemyTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    validationService = SeatValidationService(
        seat_repository=seat_repository, theater_repository=theather_repository
    )

    return CreateTheaterSeatUseCase(
        seat_repository=seat_repository, validation_service=validationService
    )


async def update_theater_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> UpdateTheaterSeatUseCase:
    """
    Dependency for SaveTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SQLAlchemyTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    validationService = SeatValidationService(
        seat_repository=seat_repository, theater_repository=theather_repository
    )

    return UpdateTheaterSeatUseCase(
        seat_repository=seat_repository, validation_service=validationService
    )


async def delete_theater_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteTheaterSeatUseCase:
    """
    Dependency for DeleteTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SQLAlchemyTheaterSeatRepository(db)

    return DeleteTheaterSeatUseCase(repository)
