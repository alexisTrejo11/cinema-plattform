from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enums.theather_enum import TheaterType
from .theather_seat import TheaterSeat


class Theater(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    theater_id: int = Field(gt=0)
    cinema_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=50)
    capacity: int = Field(gt=0)
    theater_type: TheaterType
    seats: List[TheaterSeat] = Field(default_factory=list)
    is_active: bool = True
    maintenance_mode: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def get_name(self) -> str:
        return self.name

    def get_seats(self) -> List[TheaterSeat]:
        return self.seats

    def get_seat_by_id(self, seat_id: int) -> Optional[TheaterSeat]:
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat
        return None

    def save_seats(self, seats: List[TheaterSeat]) -> None:
        self.seats = seats
        self.updated_at = datetime.now()

    def update(self, theater: 'Theater') -> None:
        self.name = theater.name
        self.capacity = theater.capacity
        self.theater_type = theater.theater_type
        self.is_active = theater.is_active
        self.maintenance_mode = theater.maintenance_mode
        self.updated_at = datetime.now()
        self.save_seats(theater.seats)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
