from typing import Any
from app.shared.base_exceptions import NotFoundException, ValidationException


class TicketNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("Ticket", entity_id)


class TicketInvalidOperationError(ValidationException):
    def __init__(self, field: str, reason: str):
        super().__init__(field, reason)


class ShowtimeNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("Showtime", entity_id)


class TheaterNotFound(NotFoundException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(entity, entity_id)


class SeatNotFoundError(NotFoundException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(entity, entity_id)


class SeatInvalidIdListError(ValidationException):
    def __init__(self, field: str, reason: str):
        super().__init__(field, reason)


class SeatUnavailableError(ValidationException):
    """Raised when a seat cannot be taken (already sold or blocked)."""

    def __init__(self, seat_id: int, reason: str = "seat not available"):
        super().__init__(str(seat_id), reason)


class PaymentAuthorizationFailedError(ValidationException):
    def __init__(self, reason: str):
        super().__init__("payment", reason)
