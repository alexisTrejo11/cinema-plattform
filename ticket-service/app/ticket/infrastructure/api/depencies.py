from datetime import datetime
from typing import Optional

from fastapi import Depends, Query

from app.external.billboard.infrastructure.repository.mongo_showtime import (
    MongoShowtimeRepository,
)
from app.external.billboard.infrastructure.repository.mongo_theater_repo import (
    MongoTheaterRepository,
)
from app.ticket.domain.interfaces import TicketRepository
from app.ticket.domain.services import TicketService

from app.ticket.application.dtos import SearchTicketParams
from app.ticket.domain.valueobjects.enums import TicketStatus
from app.ticket.application.usecases.ticket_command_use_cases import (
    CancelTicketCase,
    DigitalBuyTicketsUseCase,
    UseTicketUseCase,
)
from app.ticket.application.usecases.ticket_query_use_cases import (
    GetTicketByIdUseCase,
    GetTicketsByCriteriaUseCase,
    GetTicketsByShowtimeIdUseCase,
    GetTicketsByUserIdUseCase,
)
from app.ticket.application.usecases.ticket_summary_use_cases import (
    GetPurchaseQuoteUseCase,
    GetUserTicketSummaryUseCase,
    ListShowtimeSeatsForSaleUseCase,
)
from app.ticket.infrastructure.persistence.repository import (
    SqlAlchemySeatRepository,
    SqlAlchemyTicketRepository,
)
from app.config.mongo_config import get_mongo_database
from app.config.postgres_config import get_db as get_postgres_db
from app.ticket.domain.services import ShowtimeSeatService


def get_ticket_repository(
    sesison=Depends(get_postgres_db),
) -> TicketRepository:
    return SqlAlchemyTicketRepository(sesison)


def get_seat_repository(
    sesison=Depends(get_postgres_db),
) -> SqlAlchemySeatRepository:
    return SqlAlchemySeatRepository(sesison)


def get_theater_repository(db=Depends(get_mongo_database)) -> MongoTheaterRepository:
    return MongoTheaterRepository(db)


def get_show_time_repository(db=Depends(get_mongo_database)) -> MongoShowtimeRepository:
    return MongoShowtimeRepository(db)


def get_ticket_service(
    ticket_repo=Depends(get_ticket_repository),
    theater_repo=Depends(get_theater_repository),
):
    return TicketService(ticket_repo, theater_repo)


def get_showtime_seat_service(
    repo: SqlAlchemySeatRepository = Depends(get_seat_repository),
    theater_repo=Depends(get_theater_repository),
) -> ShowtimeSeatService:
    return ShowtimeSeatService(repo, theater_repo)


def get_ticket_by_id_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> GetTicketByIdUseCase:
    return GetTicketByIdUseCase(ticket_service)


def list_ticket_by_user_id_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> GetTicketsByUserIdUseCase:
    return GetTicketsByUserIdUseCase(ticket_service)


def list_ticket_by_showtime_id_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> GetTicketsByShowtimeIdUseCase:
    return GetTicketsByShowtimeIdUseCase(ticket_service)


def search_showtimes_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> GetTicketsByCriteriaUseCase:
    return GetTicketsByCriteriaUseCase(ticket_service)


def use_ticket_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> UseTicketUseCase:
    return UseTicketUseCase(ticket_service)


def cancel_ticket_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> CancelTicketCase:
    return CancelTicketCase(ticket_service)


def buy_ticket_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
    seat_service: ShowtimeSeatService = Depends(get_showtime_seat_service),
    showtime_repo: MongoShowtimeRepository = Depends(get_show_time_repository),
) -> DigitalBuyTicketsUseCase:
    return DigitalBuyTicketsUseCase(
        ticket_service,
        seat_service,
        showtime_repo,
        payment_gateway=None,
        seat_assertion=None,
    )


def get_user_ticket_summary_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> GetUserTicketSummaryUseCase:
    return GetUserTicketSummaryUseCase(ticket_service)


def get_purchase_quote_uc(
    showtime_repo: MongoShowtimeRepository = Depends(get_show_time_repository),
) -> GetPurchaseQuoteUseCase:
    return GetPurchaseQuoteUseCase(showtime_repo)


def list_showtime_seats_uc(
    seat_service: ShowtimeSeatService = Depends(get_showtime_seat_service),
) -> ListShowtimeSeatsForSaleUseCase:
    return ListShowtimeSeatsForSaleUseCase(seat_service)


def search_ticket_params(
    movie_id: Optional[int] = Query(None, description="Filter by movie ID"),
    showtime_id: Optional[int] = Query(None, description="Filter by showtime ID"),
    user_id: Optional[int] = Query(None, description="Filter by purchaser user ID"),
    status: Optional[TicketStatus] = Query(None, description="Filter by ticket lifecycle status"),
    include_seats: bool = Query(False, description="Include seat rows on each ticket"),
    created_before: Optional[datetime] = Query(
        None, description="Tickets created strictly before this instant (ISO 8601)"
    ),
    created_after: Optional[datetime] = Query(
        None, description="Tickets created strictly after this instant (ISO 8601)"
    ),
    page_limit: int = Query(10, ge=1, le=100, description="Page size"),
    page_offset: int = Query(0, ge=0, description="Offset for pagination"),
    sort_by: str = Query(
        "created_at",
        description="Sort field: created_at, updated_at, or price (if supported by repository)",
    ),
    sort_direction_asc: bool = Query(True, description="True = ascending, False = descending"),
) -> SearchTicketParams:
    """Builds `SearchTicketParams` from query string (single OpenAPI group)."""
    return SearchTicketParams(
        movie_id=movie_id,
        showtime_id=showtime_id,
        user_id=user_id,
        status=status,
        include_seats=include_seats,
        created_before=created_before,
        created_after=created_after,
        page_limit=page_limit,
        page_offset=page_offset,
        sort_by=sort_by,
        sort_direction_asc=sort_direction_asc,
    )
