from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.promotion import Promotion, PromotionId
from ..command.promotion_result import PromotionCommandResult as CommandResult
from ..command.promotion_command import PromotionCreateCommand, ExtendPromotionCommand
from app.products.domain.repositories import ProductRepository
from app.shared.base_exceptions import DomainException
from app.products.domain.entities.product import Product
from app.promotions.domain.service.promotion_product_service import (
    PromotionProductService,
)


class CreatePromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
        promotion_product_service: PromotionProductService,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository
        self.promotion_product_service = promotion_product_service

    async def execute(self, command: PromotionCreateCommand) -> CommandResult:
        try:
            promotion = command.map_to_domain_and_validate_data()
            products = await self._get_products(promotion.applicable_product_ids)

            await self.promotion_repository.create(promotion)
            self._validate_buissness_logic(promotion, products)

            return CommandResult.success(
                promotion_id=promotion.id.to_string(),
                message="Promotion created successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error creating promotion: {str(e)}")

    async def _get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.get_by_id_in(product_ids)
        products = list(product_map.keys())
        if not len(products) == len(product_ids):
            raise DomainException("Some products not found")

        return products

    def _validate_buissness_logic(self, promotion, products):
        self.promotion_product_service.validate_promotion_rule_integrity(
            promotion, products
        )


class ExtendPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: ExtendPromotionCommand) -> CommandResult:
        try:
            promotion = await self.promotion_repository.get_by_id(command.id)
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


class DeletePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id.to_string(), message="Promotion not found"
            )

        await self.promotion_repository.delete(promotion.id)
        return CommandResult.success(
            promotion_id=promotion.id.to_string(),
            message="Promotion deleted successfully",
        )


class ApplyPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
        promotion_product_service: PromotionProductService,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository
        self.promotion_product_service = promotion_product_service

    async def execute(
        self, promotion_id: PromotionId, product_ids: list
    ) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id.to_string(), message="Promotion not found"
            )

        products = await self._get_products(product_ids)
        discount = self.promotion_product_service.apply_promotion(promotion, products)

        return CommandResult.success(
            promotion_id=promotion.id.to_string(),
            message=f"Promotion applied successfully. Discount Applied({discount})",
        )

    async def _get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.get_by_id_in(product_ids)
        products = list(product_map.keys())
        if not len(products) == len(product_ids):
            raise DomainException("Some products not found")

        return products
