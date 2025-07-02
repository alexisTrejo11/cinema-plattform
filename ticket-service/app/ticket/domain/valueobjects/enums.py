from enum import Enum

class TicketStatus(str, Enum):
    AVAILABLE = "avaialable to buy"
    RESERVED = "reserved"
    USED = "used"
    REFUND = "refunded"
    NOT_BUY = "not buy it"
    NOT_USED = "not used"
    CANCELLED = "cancelled"
