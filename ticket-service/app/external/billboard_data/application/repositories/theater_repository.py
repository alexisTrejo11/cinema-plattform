from abc import ABC, abstractmethod
from typing import Optional

from app.external.billboard_data.domain.entities.theater import Theater


class TheaterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, theater_id: int) -> Optional[Theater]:
        pass
