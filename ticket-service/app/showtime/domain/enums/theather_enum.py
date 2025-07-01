from enum import Enum

class SeatType(str, Enum):
    STANDARD = "STANDARD"
    VIP = "VIP"
    ACCESSIBLE = "ACCESSIBLE"
    PREMIUM = "PREMIUM"
    
    
class TheaterType(str, Enum):
    STANDARD = "STANDARD"
    VIP = "VIP"
    IMAX = "IMAX"
    PREMIUM = "PREMIUM"
    DOLBY_ATMOS = "DOLBY_ATMOS"

