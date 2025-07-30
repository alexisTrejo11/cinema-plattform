from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from ..promotion import Promotion, PromotionId
from app.promotions.application.queries.promotion_query import (
    GetPromotionByProductIdQuery,
)
from app.shared.pagination import PaginationMetadata, PaginationQuery


class PromotionRepository(ABC):
    """Abstract interface for the promotion repository"""

    @abstractmethod
    async def get_by_id(
        self, promotion_id: PromotionId, is_active: Optional[bool] = True
    ) -> Optional[Promotion]:
        """Gets a promotion by its ID"""
        pass

    @abstractmethod
    async def get_active_promotions(
        self, query: PaginationQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        """Gets active promotions (optionally filtered by date)"""
        pass

    @abstractmethod
    async def get_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
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
