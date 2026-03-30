from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .theater import Theater


class Cinema(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    cinema_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    address: str = Field(min_length=5)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    theaters: List[Theater] = Field(default_factory=list)

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def update_info(self, name: Optional[str] = None, address: Optional[str] = None) -> None:
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        self.updated_at = datetime.now()

    def get_theater_by_id(self, theather_id: int) -> Optional[Theater]:
        for theater in self.theaters:
            if theater.theater_id == theather_id:
                return theater
        return None

    def add_theater(self, theater: Theater) -> None:
        self.theaters.append(theater)

    def update_theater(self, updated_theater: Theater) -> None:
        for idx, theater in enumerate(self.theaters):
            if theater.theater_id == updated_theater.theater_id:
                self.theaters[idx] = updated_theater
                break

    def remove_theater(self, theater_id: int) -> bool:
        initial_len = len(self.theaters)
        self.theaters = [t for t in self.theaters if t.theater_id != theater_id]
        return len(self.theaters) != initial_len

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
