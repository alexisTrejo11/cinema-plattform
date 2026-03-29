from fastapi import Depends

from app.external.billboard_data.infrastructure.repository.mongo_showtime import (
    MongoShowtimeRepository,
)
from app.external.billboard_data.infrastructure.repository.mongo_theater_repo import (
    MongoTheaterRepository,
)
from app.external.notification.notification_service import NotificationService
from app.internal.seats.application.seat_service import ShowtimeSeatService
from app.internal.seats.infra.sql_alch_repository import SqlAlchemySeatRepository
from app.internal.ticket.application.repository import TicketRepository
from app.internal.ticket.application.service.ticket_service import TicketService
from app.internal.ticket.application.usecases.ticket_command_use_cases import (
    CancelTicketCase,
    DigitalBuyTicketsUseCase,
    UseTicketUseCase,
)
from app.internal.ticket.application.usecases.ticket_query_use_cases import (
    GetTicketByIdUseCase,
    ListTicketsByShowtimeIdUseCase,
    ListTicketsByUserIdUseCase,
    SearchSearchUseCase,
)
from app.internal.ticket.infrastructure.repository.sql_alch_ticket_repository import (
    SQLAlchemyTicketRepository,
)
from config.mongo_config import get_mongo_database
from config.postgres_config import get_postgres_db


def get_ticket_repository(
    sesison=Depends(get_postgres_db),
) -> TicketRepository:
    return SQLAlchemyTicketRepository(sesison)


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
) -> ListTicketsByUserIdUseCase:
    return ListTicketsByUserIdUseCase(ticket_service)


def list_ticket_by_showtime_id_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> ListTicketsByShowtimeIdUseCase:
    return ListTicketsByShowtimeIdUseCase(ticket_service)


def search_showtimes_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
) -> SearchSearchUseCase:
    return SearchSearchUseCase(ticket_service)


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
    notification_service = NotificationService()
    return DigitalBuyTicketsUseCase(
        ticket_service, notification_service, seat_service, showtime_repo
    )
