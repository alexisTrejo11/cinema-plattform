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