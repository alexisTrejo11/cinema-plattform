from fastapi import Depends

from app.external.billboard_data.infrastructure.repository.mongo_showtime import (
    MongoShowtimeRepository,
)
from app.external.billboard_data.infrastructure.repository.mongo_theater_repo import (
    MongoTheaterRepository,
)
from app.ticket.domain.interfaces import TicketRepository
from app.ticket.domain.services import TicketService

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
    return DigitalBuyTicketsUseCase(ticket_service, seat_service, showtime_repo)
