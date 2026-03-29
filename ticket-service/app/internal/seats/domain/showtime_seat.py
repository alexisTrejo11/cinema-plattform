from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ShowtimeSeat(BaseModel):
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "showtime_id": self.showtime_id,
            "seat_id": self.seat_id,
            "seat_name": self.seat_name,
            "is_available": self.is_available,
            "created_at": self.created_at,
            "taken_at": self.taken_at,
            "ticket_id": self.ticket_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShowtimeSeat":
        return cls(
            showtime_id=data["showtime_id"],
            seat_id=data["seat_id"],
            seat_name=data["seat_name"],
            is_available=data.get("is_available", True),
            created_at=data.get("created_at"),
            taken_at=data.get("taken_at"),
            ticket_id=data.get("ticket_id"),
            id=data.get("id"),
        )

    def ocuppy(self) -> None:
        if not self.is_available:
            raise ValueError(f"Seat {self.id} already taken")
        self.taken_at = datetime.now(timezone.utc)
        self.is_available = False

    def release(self) -> None:
        self.taken_at = None
        self.is_available = True
        self.ticket_id = None
