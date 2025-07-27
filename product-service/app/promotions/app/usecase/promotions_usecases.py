from .promotion_command_usecases import (
    CreatePromotionUseCase,
    ActivatePromotionUseCase,
    DeactivatePromotionUseCase,
    ExtendPromotionUseCase,
)
from .promotion_query_usecases import (
    GetActivePromotionsUseCase,
    GetPromotionByIdUseCase,
    GetPromotionByProductIdUseCase,
)
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.products.domain.repositories import ProductRepository
from ..command.promotion_command import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
)
from ..command.promotion_result import PromotionCommandResult as CommandResult
from ..queries.promotion_query import (
    PaginationQuery,
    PromotionQuery,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
    PromotionId,
)
from ..queries.promotion_response import PromotionResponse, PromotionSearchResponse


class PromotionsUseCases:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.create = CreatePromotionUseCase(promotion_repository, product_repository)
        self.activate = ActivatePromotionUseCase(promotion_repository)
        self.deactivate = DeactivatePromotionUseCase(promotion_repository)
        self.extend = ExtendPromotionUseCase(promotion_repository)
        self.get_active = GetActivePromotionsUseCase(
            promotion_repository, product_repository
        )
        self.get_by_id = GetPromotionByIdUseCase(
            promotion_repository, product_repository
        )
        self.get_by_product = GetPromotionByProductIdUseCase(
            promotion_repository, product_repository
        )

    async def create_promotion(self, command: PromotionCreateCommand) -> CommandResult:
        return await self.create.execute(command)

    async def activate_promotion(self, promotion_id: PromotionId) -> CommandResult:
        return await self.activate.execute(promotion_id)

    async def deactivate_promotion(self, promotion_id: PromotionId) -> CommandResult:
        return await self.deactivate.execute(promotion_id)

    async def extend_promotion(self, command: ExtendPromotionCommand) -> CommandResult:
        return await self.extend.execute(command)

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
