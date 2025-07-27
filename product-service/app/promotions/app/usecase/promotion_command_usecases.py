from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.promotion import Promotion, PromotionId
from ..command.promotion_result import PromotionCommandResult as CommandResult
from ..command.promotion_command import PromotionCreateCommand, ExtendPromotionCommand
from app.products.domain.repositories import ProductRepository
from app.shared.base_exceptions import DomainException
from app.products.domain.entities.product import Product
from app.promotions.domain.service.

class CreatePromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(self, command: PromotionCreateCommand) -> CommandResult:
        try:
            promotion = command.to_domain()
            promotion.validate_creation()
        
            await self.validate_products(promotion.applicable_product_ids)

            await self.promotion_repository.create(promotion)

            return CommandResult.success(
                promotion_id=promotion.id.to_string(),
                message="Promotion created successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error creating promotion: {str(e)}")

    async def validate_products(self, product_ids: list) -> None:
        products = await self.product_repository.get_by_id_in(product_ids)
        if not len(products) == len(product_ids):
            raise DomainException("Some products not found")


class ExentdPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: ExtendPromotionCommand) -> CommandResult:
        try:
            promotion = await self.promotion_repository.get_by_id(command.id``)
            if not promotion:
                return CommandResult.error(
                    promotion_id=command.id.to_string(), message="Promotion not found"
                )

            promotion.extend_validity(command.available_until)
            await self.promotion_repository.update(promotion)

            return CommandResult.success(
                promotion_id=promotion.id.to_string(),
                message="Promotion updated successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error updating promotion: {str(e)}")


class ActivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        try:
            promotion = await self.promotion_repository.get_by_id(promotion_id)
            if not promotion:
                return CommandResult.error(
                    promotion_id=promotion_id.to_string(), message="Promotion not found"
                )

            promotion.activate()
            await self.promotion_repository.update(promotion)

            return CommandResult.success(
                promotion_id=promotion.id.to_string(),
                message="Promotion activated successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error activating promotion: {str(e)}")


class DeactivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id.to_string(), message="Promotion not found"
            )

        promotion.deactivate()
        await self.promotion_repository.update(promotion)

        return CommandResult.success(
            promotion_id=promotion.id.to_string(),
            message="Promotion deactivated successfully",
        )
