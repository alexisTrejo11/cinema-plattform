from datetime import date
from typing import Any, Optional
from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from app.core.cinema.domain.enums import LocationRegion, CinemaType, CinemaStatus
from app.core.cinema.application.dtos import SearchCinemaFilters
from app.core.cinema.application.usecases import (
    GetCinemaByIdUseCase,
    ListActiveCinemasUseCase,
    SearchCinemasUseCase,
    CreateCinemaUseCase,
    UpdateCinemaUseCase,
    DeleteCinemaUseCase,
    RestoreCinemaUseCase,
)
from app.core.cinema.infrastructure.persistence.sqlalchemy import (
    SQLAlchemyCinemaRepository,
)
import logging


# Query
async def get_cinema_by_id_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetCinemaByIdUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return GetCinemaByIdUseCase(repo)


async def get_active_cinemas_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListActiveCinemasUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return ListActiveCinemasUseCase(repo)


async def search_cinemas_use_case(
    db: AsyncSession = Depends(get_db),
) -> SearchCinemasUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return SearchCinemasUseCase(repo)


# Command
async def create_cinema_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return CreateCinemaUseCase(repo)


async def update_cinema_use_case(
    db: AsyncSession = Depends(get_db),
) -> UpdateCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return UpdateCinemaUseCase(repo)


async def delete_cinema_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return DeleteCinemaUseCase(repo)


async def restore_cinema_use_case(
    db: AsyncSession = Depends(get_db),
) -> RestoreCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return RestoreCinemaUseCase(repo)


# Filter
async def get_filters(
    name: Optional[str] = Query(None),
    tax_number: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    min_screens: Optional[int] = Query(None, ge=0),
    max_screens: Optional[int] = Query(None, ge=0),
    type: Optional[CinemaType] = Query(None),
    status: Optional[CinemaStatus] = Query(None),
    region: Optional[LocationRegion] = Query(None),
    has_parking: Optional[bool] = Query(None),
    has_food_court: Optional[bool] = Query(None),
    renovated_after: Optional[date] = Query(None),
    renovated_before: Optional[date] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    phone: Optional[str] = Query(None),
    email_contact: Optional[str] = Query(None),
) -> SearchCinemaFilters:
    return SearchCinemaFilters(
        name=name,
        tax_number=tax_number,
        is_active=is_active,
        min_screens=min_screens,
        max_screens=max_screens,
        type=type,
        status=status,
        region=region,
        has_parking=has_parking,
        has_food_court=has_food_court,
        renovated_after=renovated_after,
        renovated_before=renovated_before,
        latitude=latitude,
        longitude=longitude,
        phone=phone,
        email_contact=email_contact,
    )


logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")


def get_route_logger(request: Request) -> Any:
    def route_logger(action: str, **kwargs: Any):
        audit_logger.info(
            action,
            extra={
                "props": {
                    "path": request.url.path,
                    "method": request.method,
                    "client": request.client.host if request.client else None,
                    **kwargs,
                }
            },
        )

    return route_logger
