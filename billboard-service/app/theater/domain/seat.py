from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .enums import SeatType

class TheaterSeatBase(BaseModel):
    """
    Base schema for TheaterSeat, containing common attributes for creation/update.
    """
    theater_id: int = Field(..., description="The ID of the theater this seat belongs to.")
    seat_row: str = Field(..., max_length=5, description="The row identifier of the seat (e.g., 'A', 'AA', 'SEC1').")
    seat_number: int = Field(..., gt=0, description="The number of the seat within its row.")
    seat_type: SeatType = Field(SeatType.STANDARD, description="The classification type of the seat (e.g., STANDARD, VIP, ACCESSIBLE).")
    is_active: bool = Field(True, description="Indicates if the seat is currently active and usable.")


class TheaterSeat(TheaterSeatBase):
    """
    Full schema for a TheaterSeat, including database-generated fields.
    """
    id: Optional[int] = Field(None, description="The unique identifier of the theater seat.")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was created.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was last updated.")