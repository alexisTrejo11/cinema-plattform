import logging
from typing import Any, Dict

from app.shared.base_exceptions import NotFoundException
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository as CategoryRepository,
)
from app.promotions.domain.entities.promotion import Promotion
from app.promotions.domain.exceptions.promotion_exceptions import (
    InactivePromotionNotFoundError,
    PromotionCatalogProductsNotFoundError,
    PromotionNotFoundError,
)
from app.promotions.domain.factory.promotion_rule_factory import PromotionRuleFactory
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.entities.promotion import PromotionId
from app.promotions.domain.entities.value_objects import PromotionType
from ..commands import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)

logger = logging.getLogger("app")


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

    async def execute(self, command: PromotionCreateCommand) -> Promotion:
        promotion = command.map_to_domain()
        promotion.validate_creation_fields()

        promotion.rule = self.create_rule(command.rule, promotion.promotion_type)

        if command.applicable_product_ids:
            promotion.applicable_product_ids = await self.get_products(
                command.applicable_product_ids
            )

        if command.applicable_category_id:
            await self.get_category(command.applicable_category_id)

        await self.promotion_repository.create(promotion)

        logger.info(
            "Promotion created",
            extra={
                "props": {
                    "event": "promotion_created",
                    "promotion_id": str(promotion.id),
                }
            },
        )
        return promotion

    async def get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.find_by_id_in(product_ids)
        found = set(product_map.keys())
        missing = [pid for pid in product_ids if pid not in found]
        if missing:
            raise PromotionCatalogProductsNotFoundError(
                missing_product_ids=[str(x) for x in missing]
            )
        return list(found)

    def create_rule(self, rule: Dict[str, Any], promotion_type: PromotionType) -> dict:
        return PromotionRuleFactory.create_promotion_rule(promotion_type, rule)

    async def get_category(self, category_id: int) -> Any:
        category = await self.category_repository.find_by_id(category_id)
        if not category:
            raise NotFoundException("Category", category_id)
        return category


class ExtendPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: ExtendPromotionCommand) -> None:
        promotion = await self.promotion_repository.get_by_id(command.id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=command.id)

        promotion.extend_validity(command.available_until)
        await self.promotion_repository.update(promotion)

        logger.info(
            "Promotion validity extended",
            extra={
                "props": {
                    "event": "promotion_extended",
                    "promotion_id": str(promotion.id),
                }
            },
        )


class ActivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> None:
        promotion_deactivated = await self.promotion_repository.get_by_id(
            promotion_id, is_active=False
        )
        if not promotion_deactivated:
            raise InactivePromotionNotFoundError(promotion_id=promotion_id)

        promotion_deactivated.activate()
        await self.promotion_repository.update(promotion_deactivated)

        logger.info(
            "Promotion activated",
            extra={
                "props": {
                    "event": "promotion_activated",
                    "promotion_id": str(promotion_deactivated.id),
                }
            },
        )


class DeactivatePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> None:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=promotion_id)

        promotion.deactivate()
        await self.promotion_repository.update(promotion)

        logger.info(
            "Promotion deactivated",
            extra={
                "props": {
                    "event": "promotion_deactivated",
                    "promotion_id": str(promotion.id),
                }
            },
        )


class DeletePromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> None:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=promotion_id)

        await self.promotion_repository.delete(promotion.id)

        logger.info(
            "Promotion deleted",
            extra={
                "props": {
                    "event": "promotion_deleted",
                    "promotion_id": str(promotion.id),
                }
            },
        )


class ApplyPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(self, promotion_id: PromotionId, product_ids: list) -> None:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=promotion_id)

        await self._get_products(product_ids)
        promotion.validate_applicable_products(product_ids)
        promotion.apply(len(product_ids))
        await self.promotion_repository.update(promotion)

        logger.info(
            "Promotion applied",
            extra={
                "props": {
                    "event": "promotion_applied",
                    "promotion_id": str(promotion.id),
                    "product_count": len(product_ids),
                }
            },
        )

    async def _get_products(self, product_ids: list) -> list:
        product_map = await self.product_repository.find_by_id_in(product_ids)
        found = set(product_map.keys())
        missing = [pid for pid in product_ids if pid not in found]
        if missing:
            raise PromotionCatalogProductsNotFoundError(
                missing_product_ids=[str(x) for x in missing]
            )
        return list(found)


class RemoveProductsPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: RemoveProductsPromotionCommand) -> None:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=command.promotion_id)

        promotion.remove_applicable_products(command.product_ids)
        await self.promotion_repository.update(promotion)

        logger.info(
            "Products removed from promotion",
            extra={
                "props": {
                    "event": "promotion_products_removed",
                    "promotion_id": str(promotion.id),
                    "product_ids": [str(p) for p in command.product_ids],
                }
            },
        )


class RemoveCategoryPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, command: RemoveCategoryPromotionCommand) -> None:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=command.promotion_id)

        promotion.remove_applicable_category(command.category_id)
        await self.promotion_repository.update_categories(
            promotion.id, promotion.applicable_categories_ids
        )

        logger.info(
            "Category removed from promotion",
            extra={
                "props": {
                    "event": "promotion_category_removed",
                    "promotion_id": str(promotion.id),
                    "category_id": command.category_id,
                }
            },
        )


class ClearPromotionUseCase:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def execute(self, promotion_id: PromotionId) -> None:
        promotion = await self.promotion_repository.get_by_id(promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=promotion_id)

        promotion.clear_all()
        await self.promotion_repository.update(promotion)
        await self.promotion_repository.update_categories(promotion.id, [])
        await self.promotion_repository.update_products(promotion.id, [])

        logger.info(
            "Promotion cleared",
            extra={
                "props": {
                    "event": "promotion_cleared",
                    "promotion_id": str(promotion.id),
                }
            },
        )


class AddProductsToPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        product_repository: ProductRepository,
    ):
        self.promotion_repository = promotion_repository
        self.product_repository = product_repository

    async def execute(self, add_products_command: AddProductsPromotionCommand) -> None:
        promotion = await self.promotion_repository.get_by_id(
            add_products_command.promotion_id
        )
        if not promotion:
            raise PromotionNotFoundError(promotion_id=add_products_command.promotion_id)

        products = await self.product_repository.find_by_id_in(
            add_products_command.product_ids
        )
        if len(products) != len(add_products_command.product_ids):
            found = set(products.keys())
            missing = [
                pid for pid in add_products_command.product_ids if pid not in found
            ]
            raise PromotionCatalogProductsNotFoundError(
                missing_product_ids=[str(x) for x in missing]
            )

        promotion.add_applicable_products(add_products_command.product_ids)
        await self.promotion_repository.update(promotion)

        logger.info(
            "Products added to promotion",
            extra={
                "props": {
                    "event": "promotion_products_added",
                    "promotion_id": str(promotion.id),
                    "product_ids": [str(p) for p in add_products_command.product_ids],
                }
            },
        )


class AddCategoryPromotionUseCase:
    def __init__(
        self,
        promotion_repository: PromotionRepository,
        category_repository: CategoryRepository,
    ):
        self.promotion_repository = promotion_repository
        self.category_repository = category_repository

    async def execute(self, command: AddCategoryPromotionCommand) -> None:
        promotion = await self.promotion_repository.get_by_id(command.promotion_id)
        if not promotion:
            raise PromotionNotFoundError(promotion_id=command.promotion_id)

        category = await self.category_repository.find_by_id(command.category_id)
        if not category:
            raise NotFoundException("Category", command.category_id)

        promotion.add_applicable_category(command.category_id)
        await self.promotion_repository.update_categories(
            promotion.id, promotion.applicable_categories_ids
        )

        logger.info(
            "Category added to promotion",
            extra={
                "props": {
                    "event": "promotion_category_added",
                    "promotion_id": str(promotion.id),
                    "category_id": command.category_id,
                }
            },
        )
