from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db

# REPO
from app.showtime.infrastructure.persistence.sqlalchemy import (
    SQLAlchemyShowtimeRepository,
    SQLAlchemyShowtimeSeatRepository,
)
from app.showtime.infrastructure.grpc import GrpcCatalogGateway

# USECASE
from app.showtime.application.use_cases import (
    LaunchShowtimeUseCase,
    DraftShowtimeUseCase,
    CancelShowtimeUseCase,
    RestoreShowtimeUseCase,
    UpdateShowtimeUseCase,
    DeleteShowtimeUseCase,
    SearchShowtimesUseCase,
    GetShowtimeByIdUseCase,
    ListShowtimeSeatsUseCase,
    GetShowtimeSeatByIdUseCase,
    TakeSeatUseCase,
    CancelSeatUseCase,
)

# DOMAIN SERVICES
from app.showtime.domain.services import (
    ShowtimeValidationService,
    ShowTimeSeatService,
)


# COMMAND SHOWTIME
async def launch_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> LaunchShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return LaunchShowtimeUseCase(showtime_repo)


async def update_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> UpdateShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    catalog_gateway = GrpcCatalogGateway()
    validation_service = ShowtimeValidationService(showtime_repo, catalog_gateway)
    return UpdateShowtimeUseCase(showtime_repo, validation_service)


async def draft_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> DraftShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    catalog_gateway = GrpcCatalogGateway()
    validation_service = ShowtimeValidationService(showtime_repo, catalog_gateway)
    showtime_seat_service = ShowTimeSeatService(catalog_gateway, showtime_seat_repo)
    return DraftShowtimeUseCase(
        showtime_repo, validation_service, showtime_seat_service
    )


async def cancel_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> CancelShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return CancelShowtimeUseCase(showtime_repo)


async def restore_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> RestoreShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return RestoreShowtimeUseCase(showtime_repo)


async def delete_showtime_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return DeleteShowtimeUseCase(showtime_repo)


# QUERIES SHOWTIME
async def search_showtimes_use_case(
    db: AsyncSession = Depends(get_db),
) -> SearchShowtimesUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return SearchShowtimesUseCase(showtime_repo)


async def get_showtime_by_id_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetShowtimeByIdUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimeByIdUseCase(showtime_repo)


# SEAT
async def get_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetShowtimeSeatByIdUseCase:
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    return GetShowtimeSeatByIdUseCase(showtime_seat_repo)


async def list_showtimes_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListShowtimeSeatsUseCase:
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return ListShowtimeSeatsUseCase(showtime_seat_repo, showtime_repo)


async def take_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> TakeSeatUseCase:
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    return TakeSeatUseCase(showtime_seat_repo)


async def cancel_showtime_seat_use_case(
    db: AsyncSession = Depends(get_db),
) -> CancelSeatUseCase:
    showtime_seat_repo = SQLAlchemyShowtimeSeatRepository(db)
    return CancelSeatUseCase(showtime_seat_repo)
