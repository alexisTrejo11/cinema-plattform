from typing import Any, Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict, field
from app.external.billboard_data.domain.entities.theater import Theater

@dataclass(frozen=True)
class Cinema:
    """Represents a cinema location in the domain model.
    
    Attributes:
        id: Unique identifier for the cinema (positive integer)
        name: Name of the cinema (non-empty string)
        address: Physical address of the cinema (non-empty string)
        is_active: Whether the cinema is operational (default True)
        created_at: Timestamp of creation (default current time)
        updated_at: Timestamp of last update (default current time)
    """
    cinema_id: int
    name: str
    address: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    theaters: List[Theater] = field(default_factory=list)     
    
    def __post_init__(self):
        """Validate the cinema attributes after initialization."""
        self._validate_id(self.cinema_id)
        self._validate_name(self.name)
        self._validate_address(self.address)

    @staticmethod
    def _validate_id(value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID must be a positive integer")

    @staticmethod
    def _validate_name(value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")

    @staticmethod
    def _validate_address(value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 5:
            raise ValueError("Address must be a string with at least 5 characters")


    def activate(self) -> None:
        object.__setattr__(self, 'is_active', True)
        object.__setattr__(self, 'updated_at', datetime.now())

    def deactivate(self) -> None:
        object.__setattr__(self, 'is_active', False)
        object.__setattr__(self, 'updated_at', datetime.now())

    def update_info(self, name: Optional[str] = None, address: Optional[str] = None) -> None:
        """Actualiza nombre/dirección (si se proporcionan)."""
        if name is not None:
            self._validate_name(name)
            object.__setattr__(self, 'name', name)
        if address is not None:
            self._validate_address(address)
            object.__setattr__(self, 'address', address)
        object.__setattr__(self, 'updated_at', datetime.now())


    def get_theater_by_id(self, theather_id: int) -> Optional[Theater]:
        for theater in self.theaters:
            if theater.theater_id == theather_id:
                return theater

        return None
    
    
    def add_theater(self, theater: Theater) -> None:
        self.theaters.append(theater)


    def update_theater(self, updated_theater: Theater) -> None:
        for i, theater in enumerate(self.theaters):
            if theater.theater_id == updated_theater.theater_id:
                self.theaters[i] = updated_theater
                break   
    
    
    def remove_theater(self, theater_id: int) -> bool:
        initial_len = len(self.theaters)
        updated_theaters = [t for t in self.theaters if t.theater_id != theater_id]
        object.__setattr__(self, 'theaters', updated_theaters)
        return len(self.theaters) != initial_len
    

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)