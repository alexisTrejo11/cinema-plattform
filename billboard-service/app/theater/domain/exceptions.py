from app.shared.exceptions import DomainException

class TheaterError(DomainException):
    """Base exception for theater-related errors"""
    pass

class TheaterMaintenanceError(TheaterError):
    """Raised when trying to activate a theater in maintenance"""
    pass

class InvalidCapacityError(TheaterError):
    """Raised when capacity is outside allowed range for theater type"""
    pass