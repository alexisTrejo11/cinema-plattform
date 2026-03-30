from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.ticket.domain.exceptions import SeatUnavailableError


class ShowtimeSeat(BaseModel):
    """
    Represents a seat in a showtime. For each theater seat, there is a showtime seat every showtime.

    Attributes:
        showtime_id: The ID of the showtime.
        seat_id: The ID of the theater seat.
        seat_name: The name of the seat.
        is_available: Whether the seat is available.
        created_at: The datetime when the seat was created.
        taken_at: The datetime when the seat was taken.
        ticket_id: The ID of the ticket that the seat is associated with.
        id: The ID of the seat.
    """

    model_config = ConfigDict(frozen=False)

    showtime_id: int = Field(gt=0)
    seat_id: int = Field(gt=0)
    seat_name: str = Field(description="e.g., 'C4', 'F11'")
    is_available: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    taken_at: Optional[datetime] = None
    ticket_id: Optional[int] = None
    id: Optional[int] = None

    @field_validator("seat_name")
    @classmethod
    def seat_name_non_empty(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise ValueError("seat_name must be a non-empty string.")
        return str(v).strip()

    @field_validator("ticket_id")
    @classmethod
    def ticket_id_positive_or_none(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("ticket_id must be a positive integer or None.")
        return v

    def to_seat_info_dict(self) -> Dict[str, Any]:
        """Payload shape for API SeatInfo / TicketResponse."""
        parts = self.seat_name.split("-", 1)
        row = parts[0] if parts else ""
        try:
            number = int(parts[1]) if len(parts) > 1 else 0
        except ValueError:
            number = 0
        return {
            "id": self.id if self.id is not None else 0,
            "seat_number": self.seat_name,
            "row": row,
            "number": number,
            "type": "Standard",
        }

    def get_id(self) -> Optional[int]:
        return self.id

    def get_showtime_id(self) -> int:
        return self.showtime_id

    def get_seat_id(self) -> int:
        return self.seat_id

    def get_seat_name(self) -> str:
        return self.seat_name

    def get_is_available(self) -> bool:
        return self.is_available

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_taken_at(self) -> Optional[datetime]:
        return self.taken_at

    def get_ticket_id(self) -> Optional[int]:
        return self.ticket_id

    def ocuppy(self) -> None:
        if not self.is_available:
            sid = self.id if self.id is not None else 0
            raise SeatUnavailableError(sid, "already taken")
        self.taken_at = datetime.now(timezone.utc)
        self.is_available = False

    def release(self) -> None:
        self.taken_at = None
        self.is_available = True
        self.ticket_id = None
