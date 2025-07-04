from datetime import datetime, timezone
from typing import Optional, Dict, Any

class ShowtimeSeat:
    def __init__(
        self,
        showtime_id: int,
        seat_id: int,
        seat_name: str, # e.g., "C4", "F11"
        is_available: bool = True,
        created_at: Optional[datetime] = None,
        taken_at: Optional[datetime] = None,
        ticket_id: Optional[int] = None,
        id: Optional[int] = None,
    ):
        if not isinstance(showtime_id, int) or showtime_id <= 0:
            raise ValueError("showtime_id must be a positive integer.")
        if not isinstance(seat_id, int) or seat_id <= 0:
            raise ValueError("seat_id must be a positive integer.")
        if not isinstance(seat_name, str) or not seat_name.strip():
            raise ValueError("seat_name must be a non-empty string.")
        if not isinstance(is_available, bool):
            raise ValueError("is_available must be a boolean.")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("created_at must be a datetime object or None.")
        if taken_at is not None and not isinstance(taken_at, datetime):
            raise ValueError("taken_at must be a datetime object or None.")
        if ticket_id is not None and (not isinstance(ticket_id, int) or ticket_id <= 0):
            raise ValueError("ticket_id must be a positive integer or None.")

        self.__showtime_id = showtime_id
        self.__seat_id = seat_id
        self.__seat_name = seat_name
        self.__is_available = is_available
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__taken_at = taken_at
        self.__ticket_id = ticket_id
        self.__id = id

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_showtime_id(self) -> int:
        return self.__showtime_id

    def get_seat_id(self) -> int:
        return self.__seat_id

    def get_seat_name(self) -> str:
        return self.__seat_name

    def get_is_available(self) -> bool:
        return self.__is_available

    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_taken_at(self) -> Optional[datetime]:
        return self.__taken_at

    def get_ticket_id(self) -> Optional[int]:
        return self.__ticket_id

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia de ShowtimeSeat a un diccionario.
        Útil para serialización (ej. a JSON o para guardar en DB).
        """
        return {
            "id" : self.get_id(),
            "showtime_id": self.get_showtime_id(),
            "seat_id": self.get_seat_id(),
            "seat_name": self.get_seat_name(),
            "is_available": self.get_is_available(),
            "created_at": self.get_created_at(),
            "taken_at": self.get_taken_at(),
            "ticket_id": self.get_ticket_id(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            showtime_id=data["showtime_id"],
            
            seat_id=data["seat_id"],
            seat_name=data["seat_name"],
            is_available=data.get("is_available", True),
            created_at=data.get("created_at"),
            taken_at=data.get("taken_at"),
            ticket_id=data.get("ticket_id"),
        )

    def __repr__(self):
        return (f"ShowtimeSeat(showtime_id={self.__showtime_id}, "
                f"seat_name='{self.__seat_name}', available={self.__is_available})")
        
    def ocuppy(self):
        self.__taken_at = datetime.now(timezone.utc)
        
        if not self.__is_available:
            raise ValueError(f"Seat {self.__id} already taken") 
        
        self.__is_available = False
         
    def release(self):
        self.__taken_at = None    
        self.__is_available = False
        self.__ticket_id = None
