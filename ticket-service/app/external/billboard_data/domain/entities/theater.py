from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from ..enums.theather_enum import TheaterType
from .theather_seat import TheaterSeat

@dataclass(frozen=True)
class Theater:
    theater_id: int
    cinema_id: int
    name: str
    capacity: int
    theater_type: TheaterType
    seats: List[TheaterSeat] = field(default_factory=list)
    is_active: bool = True
    maintenance_mode: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not isinstance(self.theater_id, int) or self.theater_id <= 0:
            raise ValueError("ID must be a positive integer.")
        
        if not isinstance(self.cinema_id, int) or self.cinema_id <= 0:
            raise ValueError("Cinema ID must be a positive integer.")
            
        if not isinstance(self.name, str) or not (1 <= len(self.name) <= 50):
            raise ValueError("Name must be a string between 1 and 50 characters.")
            
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
            
        if not isinstance(self.theater_type, TheaterType):
            raise ValueError(f"Theater type must be a valid TheaterType enum value. Got: {self.theater_type}")
        
    
    def get_seat_by_id(self, seat_id: int) -> Optional[TheaterSeat]:
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat
        return None
    
    def save_seats(self, seats: List[TheaterSeat]) -> None:
        object.__setattr__(self, 'seats', seats)
        object.__setattr__(self, 'updated_at', datetime.now())
    
    
    def update(self, theater: 'Theater') -> None:
        object.__setattr__(self, 'name', theater.name)
        object.__setattr__(self, 'capacity', theater.capacity)
        object.__setattr__(self, 'theater_type', theater.theater_type)
        object.__setattr__(self, 'is_active', theater.is_active)
        object.__setattr__(self, 'maintenance_mode', theater.maintenance_mode)
        object.__setattr__(self, 'updated_at', datetime.now())
        self.save_seats(theater.seats)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)