from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from ..enums.theather_enum import SeatType

@dataclass(frozen=True)
class TheaterSeat:
    """Represents a seat in a theater with immutable properties.
    
    Attributes:
        seat_id: Unique identifier for the seat (positive integer)
        theater_id: ID of the theater this seat belongs to (positive integer)
        seat_row: Row identifier (1-5 character string)
        seat_number: Seat number in the row (positive integer)
        seat_type: Type of seat (STANDARD, VIP, etc.)
        is_active: Whether the seat is currently active (default True)
        created_at: Timestamp when the seat was created (default current time)
        updated_at: Timestamp when the seat was last updated (optional)
    """
    seat_id: int
    theater_id: int
    seat_row: str
    seat_number: int
    seat_type: SeatType = SeatType.STANDARD
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate all fields after initialization."""
        if not isinstance(self.theater_id, int) or self.theater_id <= 0:
            raise ValueError("Theater ID must be a positive integer.")
        
        if not isinstance(self.seat_id, int) or self.seat_id <= 0:
            raise ValueError("Seat ID must be a positive integer.")
        
        if not isinstance(self.seat_row, str) or not (1 <= len(self.seat_row) <= 5):
            raise ValueError("Seat row must be a string between 1 and 5 characters.")
        
        if not isinstance(self.seat_number, int) or self.seat_number <= 0:
            raise ValueError("Seat number must be a positive integer.")
        
        if not isinstance(self.seat_type, SeatType):
            raise ValueError(f"Seat type must be a valid SeatType enum value. Got: {self.seat_type}")
            
        if self.updated_at is not None and not isinstance(self.updated_at, datetime):
            raise ValueError("Updated at must be a datetime object or None.")


    def to_dict(self) -> Dict[str, Any]:
        """Convert the TheaterSeat to a dictionary representation.
        
        Returns:
            A dictionary containing all seat properties with proper serialization.
        """
        return asdict(self)