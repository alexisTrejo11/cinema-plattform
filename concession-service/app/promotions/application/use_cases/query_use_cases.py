from ..queries import (
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
)
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.products.domain.repositories import ProductRepository
from app.shared.pagination import PaginationQuery
from app.shared.base_exceptions import NotFoundException
from app.promotions.domain.entities.promotion import Promotion
from app.shared.pagination import Page


class GetPromotionByIdUseCase:
    """
    Use case for retrieving a promotion by its ID.
    """

    def __init__(
        self,
        promotion_query: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_query = promotion_query
        self.product_repository = product_repository

    async def execute(self, query: GetPromotionByIdQuery) -> Promotion:
        """
        Execute the use case to get a promotion by its ID.
        """
        promotion = await self.promotion_query.get_by_id(query.id)
        if not promotion:
            raise NotFoundException("Promotion", query.id.to_string())

        if query.include_products:
            await self.product_repository.find_by_id_in(
                promotion.applicable_product_ids
            )

        return promotion


class GetActivePromotionsUseCase:
    """
    Use case for retrieving active promotions.
    """

    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(self, query: PaginationQuery) -> Page[Promotion]:
        """
        Execute the use case to get a promotion by its ID.
        """
        promotion_page = await self.promotion_repository.get_active_promotions(query)

        return promotion_page


class GetPromotionByProductIdUseCase:
    """
    Use case for searching promotions based on various criteria.
    """

    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(self, query: GetPromotionByProductIdQuery) -> Page[Promotion]:
        """
        Execute the use case to search for promotions based on the provided query.
        """
        promotion_page = await self.promotion_repository.get_by_product(query)

        return promotion_page
