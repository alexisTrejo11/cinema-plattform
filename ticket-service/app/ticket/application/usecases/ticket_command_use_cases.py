import asyncio
import logging
from datetime import timedelta
from decimal import Decimal
from typing import List, Optional, Tuple

from app.ticket.application.dtos import (
    BuyTicketsRequest,
    SeatInfo,
    TicketPurchasedDetails,
)
from app.ticket.domain.entities import ShowtimeSeat
from app.ticket.domain.entities.ticket import Ticket
from app.ticket.domain.exceptions import (
    PaymentAuthorizationFailedError,
    SeatInvalidIdListError,
    SeatUnavailableError,
    ShowtimeNotFoundError,
)
from app.ticket.domain.ports import (
    PaymentAuthorizationRequest,
    PaymentGatewayPort,
    ShowtimeSeatAssertionPort,
)
from app.ticket.domain.services import ShowtimeSeatService, TicketService
from app.shared.qr import generate_ticket_qr

_log = logging.getLogger("app.ticket.application")


class DigitalBuyTicketsUseCase:
    """
    **Orchestrator** for the digital purchase flow across services and local data:

    1. Load showtime + seat rows from the local replica (Mongo/Postgres).
    2. Validate seat list locally (existence + availability flags).
    3. If a :class:`~app.ticket.domain.ports.ShowtimeSeatAssertionPort` is configured,
       call billboard (gRPC) for a **source-of-truth** concurrency check.
    4. If a :class:`~app.ticket.domain.ports.PaymentGatewayPort` is configured,
       call payment (gRPC) to **authorize** funds before mutating inventory.
    5. Take seats, persist ticket, build confirmation (QR, etc.).

    Ports are optional so dev/tests can run without remote services.
    """

    def __init__(
        self,
        ticket_service: TicketService,
        seat_service: ShowtimeSeatService,
        showtime_repo,
        payment_gateway: Optional[PaymentGatewayPort] = None,
        seat_assertion: Optional[ShowtimeSeatAssertionPort] = None,
    ) -> None:
        self.ticket_service = ticket_service
        self.seat_service = seat_service
        self.showtime_repo = showtime_repo
        self.payment_gateway = payment_gateway
        self.seat_assertion = seat_assertion

    async def execute(self, buy_dto: BuyTicketsRequest) -> TicketPurchasedDetails:
        _log.info(
            "ticket_buy_started",
            extra={
                "props": {
                    "showtime_id": buy_dto.showtime_id,
                    "customer_id": buy_dto.customer_id,
                    "seat_count": len(buy_dto.seat_list_id),
                }
            },
        )
        showtime, showtime_seats = await self._get_showtime_data(buy_dto)
        self._validate_local_seats(buy_dto, showtime_seats)

        if self.seat_assertion:
            await self.seat_assertion.assert_seats_available_for_purchase(
                buy_dto.showtime_id, list(buy_dto.seat_list_id)
            )
            _log.info(
                "seat_assertion_ok",
                extra={"props": {"showtime_id": buy_dto.showtime_id}},
            )

        if self.payment_gateway:
            total = showtime.get_price() * len(buy_dto.seat_list_id)
            idem = (
                f"{buy_dto.customer_id}:{buy_dto.showtime_id}:"
                f"{sorted(buy_dto.seat_list_id)}"
            )
            auth = await self.payment_gateway.authorize_payment(
                PaymentAuthorizationRequest(
                    amount=total,
                    currency="MXN",
                    customer_id=buy_dto.customer_id,
                    idempotency_key=idem,
                    payment_method=buy_dto.payment_method,
                    payment_token=buy_dto.payment_details,
                    customer_ip=buy_dto.customer_ip,
                )
            )
            if not auth.authorized:
                raise PaymentAuthorizationFailedError("payment not authorized")
            _log.info(
                "payment_authorized",
                extra={
                    "props": {
                        "transaction_id": auth.transaction_id,
                        "showtime_id": buy_dto.showtime_id,
                    }
                },
            )

        ticket_created = await self._process_ticket(
            buy_dto, showtime, showtime_seats
        )
        ticket_response = await self._generate_ticket_response(
            ticket_created, showtime
        )

        _log.info(
            "ticket_buy_completed",
            extra={
                "props": {
                    "ticket_id": ticket_created.id,
                    "showtime_id": buy_dto.showtime_id,
                }
            },
        )
        return ticket_response

    async def _get_showtime_data(
        self, buy_dto: BuyTicketsRequest
    ) -> Tuple[object, List[ShowtimeSeat]]:
        seats_coroutine = self.seat_service.list_by_showtime_id_and_seat_id_list(
            buy_dto.showtime_id, buy_dto.seat_list_id
        )
        showtime_coroutine = self.showtime_repo.get_by_id(
            buy_dto.showtime_id, raise_exception=False
        )

        showtime_seats, showtime = await asyncio.gather(
            seats_coroutine, showtime_coroutine
        )
        if not showtime:
            raise ShowtimeNotFoundError(buy_dto.showtime_id)
        return showtime, showtime_seats

    def _validate_local_seats(
        self, buy_dto: BuyTicketsRequest, seats: List[ShowtimeSeat]
    ) -> None:
        if len(seats) != len(buy_dto.seat_list_id):
            raise SeatInvalidIdListError(
                "seat_list_id",
                "not all seats exist for this showtime",
            )
        unavailable = [s.get_id() or 0 for s in seats if not s.is_available]
        if unavailable:
            raise SeatUnavailableError(
                unavailable[0],
                "one or more seats are not available locally",
            )

    async def _process_ticket(self, buy_dto: BuyTicketsRequest, showtime, seats):
        await self.seat_service.take_seats(buy_dto.seat_list_id)
        ticket = await self.ticket_service.create_ticket(showtime, buy_dto)
        ticket.seats = seats
        return ticket

    async def _generate_ticket_response(
        self, ticket: Ticket, showtime
    ) -> TicketPurchasedDetails:
        qr = generate_ticket_qr(
            ticket_id=str(ticket.id),
            showtime_date=showtime.get_start_time() + timedelta(minutes=30),
        )
        seat_info = [SeatInfo(**seat.to_seat_info_dict()) for seat in ticket.seats]

        txn = (
            str(ticket.payment_details.transaction_id) if ticket.payment_details else ""
        )

        return TicketPurchasedDetails.of(ticket, showtime, seat_info, qr, txn)


class UseTicketUseCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, ticket_id: int) -> None:
        _log.info("ticket_use_started", extra={"props": {"ticket_id": ticket_id}})
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        await self.ticket_service.use_ticket(ticket)
        _log.info("ticket_use_completed", extra={"props": {"ticket_id": ticket_id}})


class CancelTicketCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, ticket_id: int) -> None:
        _log.info("ticket_cancel_started", extra={"props": {"ticket_id": ticket_id}})
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        await self.ticket_service.cancel_ticket(ticket)
        _log.info("ticket_cancel_completed", extra={"props": {"ticket_id": ticket_id}})


# Backward-compatible alias
CreateTicketsUseCase = DigitalBuyTicketsUseCase
