from abc import ABC, abstractmethod
from typing import List, Optional
from app.combos.domain.entities.combo import Combo
from app.combos.application.queries import GetCombosByProductIdQuery, GetComboByIdQuery
from app.shared.pagination import PaginationQuery
from app.combos.domain.entities.value_objects import ComboId


class ComboRepository(ABC):
    @abstractmethod
    async def get_by_id(self, search_query: GetComboByIdQuery) -> Optional[Combo]:
        pass

    @abstractmethod
    async def list_by_product(
        self, search_query: GetCombosByProductIdQuery
    ) -> List[Combo]:
        pass

    @abstractmethod
    async def list(self, pagination: PaginationQuery) -> List[Combo]:
        pass

    @abstractmethod
    async def save(self, combo: Combo) -> Combo:
        pass

    @abstractmethod
    async def soft_delete(self, combo_id: ComboId) -> None:
        pass
