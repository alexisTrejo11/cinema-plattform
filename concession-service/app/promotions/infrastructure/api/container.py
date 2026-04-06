from typing import List
from app.shared.pagination import Page
from app.promotions.application.use_cases import (
    CreatePromotionUseCase,
    ActivatePromotionUseCase,
    DeactivatePromotionUseCase,
    ExtendPromotionUseCase,
    ApplyPromotionUseCase,
    DeletePromotionUseCase,
    ClearPromotionUseCase,
    AddCategoryPromotionUseCase,
    RemoveCategoryPromotionUseCase,
    AddProductsToPromotionUseCase,
    RemoveProductsPromotionUseCase,
)
from app.promotions.application.use_cases import (
    GetActivePromotionsUseCase,
    GetPromotionByIdUseCase,
    GetPromotionByProductIdUseCase,
)
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.entities.promotion import Promotion

from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.promotions.application.commands import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
)

from app.promotions.application.queries import (
    PaginationQuery,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
    PromotionId,
)
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.commands import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)


class PromotionsUseCasesContainer:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ):
        # Promotion queries
        self.get_active = GetActivePromotionsUseCase(
            promotion_repository, product_repository
        )
        self.get_by_id = GetPromotionByIdUseCase(
            promotion_repository, product_repository
        )
        self.get_by_product = GetPromotionByProductIdUseCase(
            promotion_repository, product_repository
        )

        # Basic command operations
        self.create = CreatePromotionUseCase(
            promotion_repository, product_repository, category_repository
        )
        self.activate = ActivatePromotionUseCase(promotion_repository)
        self.deactivate = DeactivatePromotionUseCase(promotion_repository)
        self.extend = ExtendPromotionUseCase(promotion_repository)
        self.apply = ApplyPromotionUseCase(promotion_repository, product_repository)
        self.clear = ClearPromotionUseCase(promotion_repository)
        self.delete = DeletePromotionUseCase(promotion_repository)

        # Add and remove products and categories from promotions
        self.add_products = AddProductsToPromotionUseCase(
            promotion_repository, product_repository
        )
        self.add_category = AddCategoryPromotionUseCase(
            promotion_repository, category_repository
        )
        self.remove_products = RemoveProductsPromotionUseCase(promotion_repository)
        self.remove_category = RemoveCategoryPromotionUseCase(promotion_repository)

    async def create_promotion(self, command: PromotionCreateCommand) -> Promotion:
        return await self.create.execute(command)

    async def activate_promotion(self, promotion_id: PromotionId) -> None:
        await self.activate.execute(promotion_id)

    async def deactivate_promotion(self, promotion_id: PromotionId) -> None:
        await self.deactivate.execute(promotion_id)

    async def extend_promotion(self, command: ExtendPromotionCommand) -> None:
        await self.extend.execute(command)

    async def clear_promotions(self, promotion_id: PromotionId) -> None:
        await self.clear.execute(promotion_id)

    async def get_active_promotions(
        self, pagination: PaginationQuery
    ) -> Page[Promotion]:
        return await self.get_active.execute(pagination)

    async def get_promotion_by_id(self, query: GetPromotionByIdQuery) -> Promotion:
        return await self.get_by_id.execute(query)

    async def get_promotions_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Page[Promotion]:
        return await self.get_by_product.execute(query)

    async def apply_promotion(
        self, promotion_id: PromotionId, product_ids: list[ProductId]
    ) -> None:
        await self.apply.execute(promotion_id, product_ids)

    async def delete_promotion(self, promotion_id: PromotionId) -> None:
        await self.delete.execute(promotion_id)

    async def add_products_to_promotion(
        self, command: AddProductsPromotionCommand
    ) -> None:
        await self.add_products.execute(command)

    async def add_category_to_promotion(
        self, command: AddCategoryPromotionCommand
    ) -> None:
        await self.add_category.execute(command)

    async def remove_products_from_promotion(
        self, command: RemoveProductsPromotionCommand
    ) -> None:
        await self.remove_products.execute(command)

    async def remove_category_from_promotion(
        self, command: RemoveCategoryPromotionCommand
    ) -> None:
        await self.remove_category.execute(command)
