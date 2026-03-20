from enum import Enum

class LocationRegion(Enum):
    CDMX_SOUTH = 'CDMX_SOUTH'
    CDMX_NORTH = "CDMX_NORTH"
    CDMX_CENTER = "CDMX_CENTER"
    CDMX_EAST = "CDMX_EAST"
    CDMX_WEST = "CDMX_WEST"

class CinemaStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    MAINTENANCE = "MAINTENANCE"


class CinemaFeatures(Enum):
    TWO_D = "2D"
    THREE_D = "3D"
    FOUR_D = "4D"
    IMAX = "IMAX"
    VIP_SEATING = "VIP_SEATING"
    DOBLY_ATMOS = "DOBLY_ATMOS"


class CinemaType(Enum):
    VIP = "VIP"
    TRADITIONAL = "TRADITIONAL"
