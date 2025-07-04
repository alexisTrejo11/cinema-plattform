from enum import Enum

class TicketStatus(str, Enum):
    RESERVED = "reserved"
    USED = "used"
    REFUND = "refunded"
    NOT_USED = "not used"
    CANCELLED = "cancelled"


class TicketType(str, Enum):
    ON_SITE = "on_site"
    DIGITAL = "digital"