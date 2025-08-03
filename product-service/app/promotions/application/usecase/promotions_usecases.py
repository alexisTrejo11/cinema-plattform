from .promotion_command_usecases import (
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
from .promotion_query_usecases import (
    GetActivePromotionsUseCase,
    GetPromotionByIdUseCase,
    GetPromotionByProductIdUseCase,
)
from app.promotions.domain.repository.promotion_repository import PromotionRepository

from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from ..command.promotion_command import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
)

from ..command.promotion_result import PromotionCommandResult as CommandResult
from ..queries.promotion_query import (
    PaginationQuery,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
    PromotionId,
)
from ..queries.promotion_response import PromotionResponse, PromotionSearchResponse
from app.products.domain.entities.value_objects import ProductId
from ..command.add_item_promotion_command import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)


class PromotionsUseCases:
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

    async def create_promotion(self, command: PromotionCreateCommand) -> CommandResult:
        return await self.create.execute(command)

    async def activate_promotion(self, promotion_id: PromotionId) -> CommandResult:
        return await self.activate.execute(promotion_id)

    async def deactivate_promotion(self, promotion_id: PromotionId) -> CommandResult:
        return await self.deactivate.execute(promotion_id)

    async def extend_promotion(self, command: ExtendPromotionCommand) -> CommandResult:
        return await self.extend.execute(command)

    async def clear_promotions(self, promotion_id: PromotionId) -> CommandResult:
        return await self.clear.execute(promotion_id)

    async def get_active_promotions(
        self, pagination: PaginationQuery
    ) -> PromotionSearchResponse:
        return await self.get_active.execute(pagination)

    async def get_promotion_by_id(
        self, query: GetPromotionByIdQuery
    ) -> PromotionResponse:
        return await self.get_by_id.execute(query)

    async def get_promotions_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> PromotionSearchResponse:
        return await self.get_by_product.execute(query)

    async def apply_promotion(
        self, promotion_id: PromotionId, product_ids: list[ProductId]
    ) -> CommandResult:
        return await self.apply.execute(promotion_id, product_ids)

    async def delete_promotion(self, promotion_id: PromotionId) -> CommandResult:
        return await self.delete.execute(promotion_id)

    async def add_products_to_promotion(
        self, command: AddProductsPromotionCommand
    ) -> CommandResult:
        return await self.add_products.execute(command)

    async def add_category_to_promotion(
        self, command: AddCategoryPromotionCommand
    ) -> CommandResult:
        return await self.add_category.execute(command)

    async def remove_products_from_promotion(
        self, command: RemoveProductsPromotionCommand
    ) -> CommandResult:
        return await self.remove_products.execute(command)

    async def remove_category_from_promotion(
        self, command: RemoveCategoryPromotionCommand
    ) -> CommandResult:
        return await self.remove_category.execute(command)
