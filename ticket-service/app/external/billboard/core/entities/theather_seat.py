from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enums.theather_enum import SeatType


class TheaterSeat(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    seat_id: int = Field(gt=0)
    theater_id: int = Field(gt=0)
    seat_row: str = Field(min_length=1, max_length=5)
    seat_number: int = Field(gt=0)
    seat_type: SeatType = SeatType.STANDARD
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def get_seat_id(self) -> int:
        return self.seat_id

    def get_seat_row(self) -> str:
        return self.seat_row

    def get_seat_number(self) -> int:
        return self.seat_number

    def get_is_active(self) -> bool:
        return self.is_active

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
