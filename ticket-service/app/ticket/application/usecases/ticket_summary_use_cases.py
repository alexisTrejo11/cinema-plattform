import logging
from decimal import Decimal
from typing import List

from app.external.billboard.core.interfaces import ShowtimeRepository
from app.ticket.application.dtos import (
    PurchaseQuoteResponse,
    SeatInfo,
    TicketSummaryResponse,
)
from app.ticket.domain.exceptions import ShowtimeNotFoundError, TicketInvalidOperationError
from app.ticket.domain.services import ShowtimeSeatService, TicketService
from app.ticket.domain.valueobjects.enums import TicketStatus

_log = logging.getLogger("app.ticket.application")


class GetUserTicketSummaryUseCase:
    """Aggregates ticket counts for monitoring and customer account views."""

    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, user_id: int) -> TicketSummaryResponse:
        tickets = await self.ticket_service.get_user_tickets(user_id)
        active = sum(
            1
            for t in tickets
            if t.status in (TicketStatus.RESERVED, TicketStatus.NOT_USED)
        )
        used = sum(1 for t in tickets if t.status == TicketStatus.USED)
        cancelled = sum(
            1
            for t in tickets
            if t.status in (TicketStatus.CANCELLED, TicketStatus.REFUND)
        )
        _log.info(
            "ticket_summary_built",
            extra={"props": {"user_id": user_id, "total": len(tickets)}},
        )
        return TicketSummaryResponse(
            user_id=user_id,
            total_tickets=len(tickets),
            active_tickets=active,
            used_tickets=used,
            cancelled_tickets=cancelled,
        )


class GetPurchaseQuoteUseCase:
    """Price preview from replicated billboard data (no seats held)."""

    def __init__(self, showtime_repository: ShowtimeRepository) -> None:
        self.showtime_repository = showtime_repository

    async def execute(
        self, showtime_id: int, seat_count: int
    ) -> PurchaseQuoteResponse:
        if seat_count < 1:
            raise TicketInvalidOperationError(
                "seat_count", "must be at least 1"
            )
        showtime = await self.showtime_repository.get_by_id(
            showtime_id, raise_exception=False
        )
        if not showtime:
            raise ShowtimeNotFoundError(showtime_id)
        unit = showtime.get_price()
        total: Decimal = unit * seat_count
        _log.info(
            "purchase_quote",
            extra={"props": {"showtime_id": showtime_id, "seat_count": seat_count}},
        )
        return PurchaseQuoteResponse(
            showtime_id=showtime_id,
            seat_count=seat_count,
            unit_price=unit,
            currency="MXN",
            total=total,
            movie_title=showtime.get_movie().get_title(),
            showtime_starts_at=showtime.get_start_time(),
        )


class ListShowtimeSeatsForSaleUseCase:
    """Seat map from local replica (authoritative concurrency via gRPC on purchase)."""

    def __init__(self, seat_service: ShowtimeSeatService) -> None:
        self.seat_service = seat_service

    async def execute(self, showtime_id: int) -> List[SeatInfo]:
        seats = await self.seat_service.get_seats_by_showtime(showtime_id)
        _log.info(
            "showtime_seats_listed",
            extra={"props": {"showtime_id": showtime_id, "count": len(seats)}},
        )
        return [SeatInfo(**s.to_seat_info_dict()) for s in seats]
