from enum import Enum

class TheaterType(str, Enum):
    TWO_D = '2D'
    THREE_D = '3D'
    IMAX = 'IMAX'
    FOUR_DX = '4DX'
    VIP = 'VIP'

class SeatType(str, Enum):
    """
    Represents the type of a cinema seat.
    Mirrors the 'seat_type_enum' in PostgreSQL.
    """
    STANDARD = "STANDARD"
    VIP = "VIP"
    ACCESSIBLE = "ACCESSIBLE" # For disabled access
    PREMIUM = "PREMIUM"
    LOVESEAT = "LOVESEAT"