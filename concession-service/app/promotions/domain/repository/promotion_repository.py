from abc import ABC, abstractmethod
from typing import List, Optional
from app.shared.pagination import PaginationQuery, Page
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.queries import GetPromotionByProductIdQuery
from ...domain.entities.promotion import Promotion, PromotionId


class PromotionRepository(ABC):
    """Abstract interface for the promotion repository"""

    @abstractmethod
    async def get_by_id(
        self,
        promotion_id: PromotionId,
        is_active: Optional[bool] = True,
    ) -> Optional[Promotion]:
        """Gets a promotion by its ID"""
        pass

    @abstractmethod
    async def get_active_promotions(self, query: PaginationQuery) -> Page[Promotion]:
        """Gets active promotions (optionally filtered by date)"""
        pass

    @abstractmethod
    async def get_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Page[Promotion]:
        """Gets promotions applicable to a specific product"""
        pass

    @abstractmethod
    async def create(self, promotion: Promotion) -> Promotion:
        """Creates a new promotion"""
        pass

    @abstractmethod
    async def update(self, promotion: Promotion) -> Promotion:
        """Updates an existing promotion"""
        pass

    @abstractmethod
    async def delete(self, promotion_id: PromotionId) -> bool:
        """Deletes a promotion"""
        pass

    @abstractmethod
    async def apply_promotion_use(self, promotion_id: PromotionId) -> bool:
        """Records a use of the promotion (increments counter)"""
        pass

    @abstractmethod
    async def update_products(
        self, promotion_id: PromotionId, product_ids: List[ProductId]
    ) -> None:
        """Updates the products associated with a promotion"""
        pass

    @abstractmethod
    async def update_categories(
        self, promotion_id: PromotionId, category_ids: List[int]
    ) -> None:
        """Updates the categories associated with a promotion"""
        pass
