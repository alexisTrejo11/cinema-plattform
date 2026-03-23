from ..queries.promotion_query import (
    PromotionQuery,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
)
from ..queries.promotion_response import PromotionResponse, PromotionSearchResponse
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.products.domain.repositories import ProductRepository
from app.shared.pagination import PaginationQuery
from app.shared.base_exceptions import NotFoundException


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

    async def execute(self, query: GetPromotionByIdQuery) -> PromotionResponse:
        """
        Execute the use case to get a promotion by its ID.
        """
        promotion = await self.promotion_query.get_by_id(query.id)
        if not promotion:
            raise NotFoundException("Promotion", query.id.to_string())

        if not query.include_products:
            return PromotionResponse.from_domain(promotion)

        products = await self.product_repository.find_by_id_in(
            promotion.applicable_product_ids
        )
        return PromotionResponse.from_domain(promotion, list(products.values()))


class GetActivePromotionsUseCase:
    """
    Use case for retrieving active promotions.
    """

    def __init__(
        self,
        promotion_query: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_query = promotion_query
        self.product_repository = product_repository

    async def execute(self, query: PaginationQuery) -> PromotionSearchResponse:
        """
        Execute the use case to get a promotion by its ID.
        """
        promotion_page = await self.promotion_query.get_active_promotions(query)

        return PromotionSearchResponse.from_domain(
            promotion_page.items, promotion_page.metadata
        )


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

    async def execute(
        self, query: GetPromotionByProductIdQuery
    ) -> PromotionSearchResponse:
        """
        Execute the use case to search for promotions based on the provided query.
        """
        promotion_page = await self.promotion_repository.get_by_product(query)

        return PromotionSearchResponse.from_domain(
            promotion_page.items, promotion_page.metadata
        )
