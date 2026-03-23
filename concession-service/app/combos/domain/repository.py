from abc import ABC, abstractmethod
from typing import Optional
from app.combos.domain.entities.combo import Combo
from app.products.domain.entities.value_objects import ProductId
from app.shared.pagination import PaginationQuery, Page
from app.combos.domain.entities.value_objects import ComboId


class ComboRepository(ABC):
    @abstractmethod
    async def find_by_id(
        self, combo_id: ComboId, include_items: bool
    ) -> Optional[Combo]:
        pass

    @abstractmethod
    async def find_by_product(
        self,
        product_id: ProductId,
        pagination: PaginationQuery,
        include_items: bool = False,
    ) -> Page[Combo]:
        pass

    @abstractmethod
    async def find_active(self, pagination: PaginationQuery) -> Page[Combo]:
        pass

    @abstractmethod
    async def save(self, combo: Combo) -> None:
        pass

    @abstractmethod
    async def delete(self, combo_id: ComboId, soft_delete: bool = True) -> None:
        pass

    @abstractmethod
    async def find_deleted_by_id(self, combo_id: ComboId) -> Optional[Combo]:
        pass
