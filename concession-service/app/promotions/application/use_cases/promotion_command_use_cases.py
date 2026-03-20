from typing import Any, Dict
from app.shared.base_exceptions import DomainException
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository as CategoryRepository,
)
from app.promotions.domain.factory.promotion_rule_factory import PromotionRuleFactory
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.entities.promotion import PromotionId
from app.promotions.domain.entities.value_objects import PromotionType
from ..command.promotion_result import PromotionCommandResult as CommandResult
from ..command.promotion_command import PromotionCreateCommand, ExtendPromotionCommand
from ..command.add_item_promotion_command import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)


class CreatePromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, command: PromotionCreateCommand) -> CommandResult:
        try:
            promotion = command.map_to_domain()
            promotion.validate_creation_fields()

            promotion.rule = self.create_rule(command.rule, promotion.promotion_type)

            if command.applicable_product_ids:
                promotion.applicable_product_ids = await self.get_products(
                    command.applicable_product_ids
                )

            if command.applicable_category_id:
                self.get_category(command.applicable_category_id)

            await self.promotion_repository.create(promotion)

            return CommandResult.success(
                promotion.id,
                "Promotion created successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error creating promotion: {str(e)}")

    async def get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.get_by_id_in(product_ids)
        products = list(product_map.keys())
        if not len(products) == len(product_ids):
            raise DomainException("Some products not found")

        return products

    def create_rule(self, rule: Dict[str, Any], promotion_type: PromotionType) -> Any:
        promotion_rule = PromotionRuleFactory.create_promotion_rule(
            promotion_type, rule
        )
        return promotion_rule.to_dict()

    def get_category(self, category_id: int) -> Any:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise DomainException(f"Category with ID {category_id} not found")
        return category


class ExtendPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: ExtendPromotionCommand) -> CommandResult:
        try:
            promotion_id = PromotionId(command.id)
            promotion = await self.promotion_repository.get_by_id(promotion_id)
            if not promotion:
                return CommandResult.error(
                    promotion_id=promotion_id, message="Promotion not found"
                )

            promotion.extend_validity(command.available_until)
            await self.promotion_repository.update(promotion)

            return CommandResult.success(
                promotion_id=promotion.id,
                message="Promotion updated successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error updating promotion: {str(e)}")


class ActivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        try:
            promotion_deactivated = await self.promotion_repository.get_by_id(
                promotion_id, is_active=False
            )
            if not promotion_deactivated:
                return CommandResult.error(
                    promotion_id=promotion_id,
                    message="Promotion deactivated not found",
                )

            promotion_deactivated.activate()
            await self.promotion_repository.update(promotion_deactivated)

            return CommandResult.success(
                promotion_id=promotion_deactivated.id,
                message="Promotion activated successfully",
            )
        except DomainException as e:
            return CommandResult.error(message=f"Error activating promotion: {str(e)}")


class DeactivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        try:
            promotion = await self.promotion_repository.get_by_id(promotion_id)
            if not promotion:
                return CommandResult.error(
                    promotion_id=promotion_id, message="Promotion not found"
                )

            promotion.deactivate()
            await self.promotion_repository.update(promotion)

            return CommandResult.success(
                promotion_id=promotion.id,
                message="Promotion deactivated successfully",
            )
        except DomainException as e:
            return CommandResult.error(
                message=f"Error deactivating promotion: {str(e)}"
            )


class DeletePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id, message="Promotion not found"
            )

        await self.promotion_repository.delete(promotion.id)
        return CommandResult.success(
            promotion_id=promotion.id,
            message="Promotion deleted successfully",
        )


class ApplyPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(
        self, promotion_id: PromotionId, product_ids: list
    ) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id, message="Promotion not found"
            )

        if not promotion.is_active:
            return CommandResult.error(
                promotion_id=promotion_id,
                message="Promotion is not active",
            )

        promotion.validate_applicable_products(product_ids)
        promotion.apply(len(product_ids))
        products = await self._get_products(product_ids)

        return CommandResult.success(
            promotion_id=promotion.id,
            message=f"Promotion applied successfully. Discount Applied to {len(products)} products.",
        )

    async def _get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.get_by_id_in(product_ids)
        products = list(product_map.keys())
        if not len(products) == len(product_ids):
            raise DomainException("Some products not found")

        return products


class RemoveProductsPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: RemoveProductsPromotionCommand) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=command.promotion_id,
                message="Promotion not found",
            )

        promotion.remove_applicable_products(command.product_ids)
        await self.promotion_repository.update_products(
            promotion.id, command.product_ids
        )

        await self.promotion_repository.update_products(
            promotion.id, promotion.applicable_product_ids
        )

        return CommandResult.success(
            promotion_id=promotion.id,
            message="Products removed from promotion successfully",
        )


class RemoveCategoryPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: RemoveCategoryPromotionCommand) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=command.promotion_id,
                message="Promotion not found",
            )

        promotion.remove_applicable_category(command.category_id)
        await self.promotion_repository.update_categories(
            promotion.id, promotion.applicable_categories_ids
        )

        return CommandResult.success(
            promotion_id=promotion.id,
            message="Category removed from promotion successfully",
        )


class ClearPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=promotion_id, message="Promotion not found"
            )

        promotion.clear_all()
        await self.promotion_repository.update(promotion)
        await self.promotion_repository.update_categories(promotion.id, [])
        await self.promotion_repository.update_products(promotion.id, [])

        return CommandResult.success(
            promotion_id=promotion.id,
            message="Promotion cleared successfully",
        )


class AddProductsToPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(
        self, add_products_command: AddProductsPromotionCommand
    ) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(
            add_products_command.promotion_id
        )
        if not promotion:
            return CommandResult.error(
                promotion_id=add_products_command.promotion_id,
                message="Promotion not found",
            )

        products = await self.product_repository.get_by_id_in(
            add_products_command.product_ids
        )
        if len(products) != len(add_products_command.product_ids):
            return CommandResult.error(message="Some products not found")

        promotion.add_applicable_products(add_products_command.product_ids)
        await self.promotion_repository.update(promotion)

        return CommandResult.success(
            promotion_id=promotion.id,
            message="Products added to promotion successfully",
        )


class AddCategoryPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        category_repository: CategoryRepository,
    ):
        self.promotion_repository = promotion_repository
        self.category_repository = category_repository

    async def execute(self, command: AddCategoryPromotionCommand) -> CommandResult:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            return CommandResult.error(
                promotion_id=command.promotion_id,
                message="Promotion not found",
            )

        category = await self.category_repository.get_by_id(command.category_id)
        if not category:
            return CommandResult.error(
                message=f"Category with ID {command.category_id} not found"
            )

        promotion.add_applicable_category(command.category_id)
        await self.promotion_repository.update_categories(
            promotion.id, promotion.applicable_categories_ids
        )

        return CommandResult.success(
            promotion_id=promotion.id,
            message="Category added to promotion successfully",
        )
