from fastapi import Depends
from config.postgres_config import get_postgres_db
from config.mongo_config import get_mongo_database
from app.ticket.application.repository import TicketRepository
from app.ticket.application.service.ticket_service import TicketService
from app.ticket.infrastructure.repository.sql_alch_ticket_repository import SQLAlchemyTicketRepository
from app.ticket.application.usecases.ticket_query_use_cases import ListTicketsByUserIdUseCase, ListTicketsByShowtimeIdUseCase, SearchSearchUseCase, GetTicketByIdUseCase
from app.ticket.application.usecases.ticket_command_use_cases import UseTicketUseCase, CancelTicketCase, BuyTicketsUseCase

from app.showtime.infrastructure.repository.mongo_theater_repo import MongoTheaterRepository
from app.showtime.infrastructure.repository.mongo_showtime import MongoShowtimeRepository
from app.seats.application.seat_service import ShowtimeSeatService
from app.seats.infra.sql_alch_repository import SqlAlchemySeatRepository

# Repositories
def get_ticket_repository(sesison = Depends(get_postgres_db)) -> TicketRepository:
    return SQLAlchemyTicketRepository(sesison)

def get_seat_repository(sesison = Depends(get_postgres_db)) -> SqlAlchemySeatRepository:
    return SqlAlchemySeatRepository(sesison)  

def get_theater_repository(db = Depends(get_mongo_database)) -> MongoTheaterRepository:
    return MongoTheaterRepository(db)

def get_show_time_repository(db = Depends(get_mongo_database)) -> MongoShowtimeRepository:
    return MongoShowtimeRepository(db)

# Services
def get_ticket_service(ticket_repo = Depends(get_ticket_repository), theater_repo = Depends(get_theater_repository)):
    return TicketService(ticket_repo, theater_repo)

# Services
def get_showtime_seat_service(repo: SqlAlchemySeatRepository = Depends(get_seat_repository)) -> ShowtimeSeatService:
    return ShowtimeSeatService(repo)

# QUERY UC
def get_ticket_by_id_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> GetTicketByIdUseCase:
    return GetTicketByIdUseCase(ticket_service)

def list_ticket_by_user_id_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> ListTicketsByUserIdUseCase:
    return ListTicketsByUserIdUseCase(ticket_service)

def list_ticket_by_showtime_id_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> ListTicketsByShowtimeIdUseCase:
    return ListTicketsByShowtimeIdUseCase(ticket_service)

def search_showtimes_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> SearchSearchUseCase:
    return SearchSearchUseCase(ticket_service)

# Command UC
def use_ticket_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> UseTicketUseCase:
    return UseTicketUseCase(ticket_service)

def cancel_ticket_uc(ticket_service: TicketService = Depends(get_ticket_service)) -> CancelTicketCase:
    return CancelTicketCase(ticket_service)

def buy_ticket_uc(
    ticket_service: TicketService = Depends(get_ticket_service),
    seat_service : ShowtimeSeatService = Depends(get_showtime_seat_service),
    showtime_repo : MongoShowtimeRepository = Depends(get_show_time_repository)
) -> BuyTicketsUseCase:
    return BuyTicketsUseCase(ticket_service, seat_service, showtime_repo)
