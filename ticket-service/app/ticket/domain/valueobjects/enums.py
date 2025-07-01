from enum import Enum

class TicketStatus(str, Enum):
    CORRUPTED = "corrupted"
    RESERVED = "reserved"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    USED = "used"
