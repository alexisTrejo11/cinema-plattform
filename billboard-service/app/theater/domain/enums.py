from enum import Enum

class TheaterType(str, Enum):
    TWO_D = 'TWO_D'
    THREE_D = 'THREE_D'
    IMAX = 'IMAX'
    FOUR_DX = 'FOUR_DX'
    VIP = 'VIP'

class SeatType(str, Enum):
    """
    Represents the type of a cinema seat.
    Mirrors the 'seat_type_enum' in PostgreSQL.
    """
    STANDARD = "STANDARD"
    VIP = "VIP"
    FOUR_DX = 'FOUR_DX'
    ACCESSIBLE = "ACCESSIBLE" # For disabled access
    PREMIUM = "PREMIUM"
    LOVESEAT = "LOVESEAT"