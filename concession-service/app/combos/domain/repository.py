from abc import ABC, abstractmethod
from typing import List, Optional
from app.combos.domain.entities.combo import Combo
from app.combos.application.queries import GetCombosByProductIdQuery, GetComboByIdQuery
from app.shared.pagination import PaginationQuery, Page
from app.combos.domain.entities.value_objects import ComboId


class ComboRepository(ABC):
    @abstractmethod
    async def get_by_id(self, query: GetComboByIdQuery) -> Optional[Combo]:
        pass

    @abstractmethod
    async def list_by_product(self, query: GetCombosByProductIdQuery) -> Page[Combo]:
        pass

    @abstractmethod
    async def list_active(
        self, pagination: PaginationQuery, include_items: bool
    ) -> Page[Combo]:
        pass

    @abstractmethod
    async def save(self, combo: Combo) -> None:
        pass

    @abstractmethod
    async def delete(self, combo_id: ComboId, soft_delete: bool = True) -> None:
        pass
