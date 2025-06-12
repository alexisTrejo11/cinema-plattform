from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import Field
from .base import ShowtimeSeatBase

class ShowtimeSeat(ShowtimeSeatBase):
    """
    Full domain entity for a ShowtimeSeat, including database-generated fields.
    'id' is Optional when created before persistence.
    """
    id: Optional[int] = Field(None, description="The unique identifier of the showtime seat.")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was created.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was last updated.")

    
    def is_taken(self) -> bool:
        return self.taken_at is not None 

    def take(self):
        if self.is_taken():
            raise ValueError("Seat Already Taken")
        self.taken_at = datetime.now(timezone.utc)

    def leave(self):
        self.taken_at = None
        self.user_id = None

    class Config:
        from_attributes = True
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "id": 1,
                "showtime_id": 101,
                "theater_seat_id": 205,
                "taken_at": "2025-06-06T14:00:00Z",
                "transaction_id": 5001,
                "user_id": 123,
                "created_at": "2025-06-06T13:30:00Z",
                "updated_at": "2025-06-06T13:30:00Z"
            }
        }