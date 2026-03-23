import logging
from typing import List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, and_, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload


from app.shared.base_exceptions import DatabaseException
from app.shared.pagination import PaginationMetadata, PaginationQuery, Page

from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.entities.promotion import Promotion, PromotionId, ProductId
from app.promotions.application.queries.promotion_query import (
    GetPromotionByProductIdQuery,
)
from app.products.infrastructure.persistence.models.product_models import (
    ProductModel,
    ProductCategoryModel,
)
from ..model.promotion_model import (
    PromotionModel,
    PromotionCategoryModel,
    PromotionProductModel,
)
from ..model.model_mapper import promotion_model_from_domain, promotion_model_to_domain

logger = logging.getLogger(__name__)


class SQLAlchemyPromotionRepository(PromotionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(
        self,
        promotion_id: PromotionId,
        is_active: Optional[bool] = True,
    ) -> Optional[Promotion]:
        try:
            stmt = (
                select(PromotionModel)
                .where(
                    and_(
                        PromotionModel.id == str(promotion_id.value),
                        PromotionModel.is_active == is_active,
                    )
                )
                .options(
                    selectinload(PromotionModel.products),
                    selectinload(PromotionModel.categories),
                )
            )
            result = await self.session.execute(stmt)

            model = result.unique().scalar_one_or_none()
            return promotion_model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting promotion {promotion_id}: {e}")
            raise DatabaseException(f"Failed to get promotion {promotion_id}") from e

    async def get_active_promotions(self, query: PaginationQuery) -> Page[Promotion]:
        try:
            where_clause = and_(
                PromotionModel.start_date <= datetime.now(),
                PromotionModel.end_date >= datetime.now(),
                PromotionModel.is_active == True,
            )
            stmt = select(PromotionModel).where(where_clause)
            stmt = PaginationQuery.paginate_stmt(stmt, query)

            result = await self.session.execute(stmt)

            return await self.return_pageble_entities(where_clause, query, result)
        except SQLAlchemyError as e:
            logger.error(f"Error getting active promotions: {e}")
            raise DatabaseException(
                f"Failed to get active promotions: {e._sql_message}"
            )

    async def get_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Page[Promotion]:
        try:
            where_clause = and_(
                PromotionModel.id.in_(
                    select(PromotionProductModel.promotion_id).where(
                        PromotionProductModel.product_id == query.product_id.value
                    )
                ),
                PromotionModel.is_active == True,
            )

            stmt = select(PromotionModel).where(where_clause)
            stmt = PaginationQuery.paginate_stmt(stmt, query.pagination)

            result = await self.session.execute(stmt)

            return await self.return_pageble_entities(
                where_clause, query.pagination, result
            )
        except SQLAlchemyError as e:
            logger.error(
                f"Error getting promotions for product {query.product_id.to_string()}: {e}"
            )
            raise DatabaseException(
                f"Failed to get promotions for product {query.product_id.to_string()}"
            ) from e

    async def create(self, promotion: Promotion) -> Promotion:
        try:
            promotion_model = promotion_model_from_domain(promotion)

            product_models_to_associate = []
            if promotion.applicable_product_ids:

                product_ids_values = [
                    p_id.value for p_id in promotion.applicable_product_ids
                ]

                products_stmt = select(ProductModel).where(
                    ProductModel.id.in_(product_ids_values)
                )
                products_result = await self.session.execute(products_stmt)
                product_models_to_associate = list(products_result.scalars().all())

                if len(product_models_to_associate) != len(
                    promotion.applicable_product_ids
                ):
                    found_ids = {p.id for p in product_models_to_associate}
                    missing_ids = set(product_ids_values) - found_ids
                    for missing_id in missing_ids:
                        logger.warning(
                            f"Producto con ID {missing_id} no encontrado para la promoción {promotion.id.value}. No se asociará."
                        )

            promotion_model.products.extend(product_models_to_associate)

            self.session.add(promotion_model)
            await self.session.commit()

            return promotion_model_to_domain(promotion_model)
        except SQLAlchemyError as e:
            logger.error(f"Error creating promotion: {e}")
            raise DatabaseException("Failed to create promotion") from e

    async def update(self, promotion: Promotion) -> Promotion:
        """Persist scalar fields and sync many-to-many products/categories from domain."""
        try:
            async with self.session.begin_nested():
                stmt = (
                    select(PromotionModel)
                    .where(PromotionModel.id == promotion.id.value)
                    .options(
                        selectinload(PromotionModel.products),
                        selectinload(PromotionModel.categories),
                    )
                )
                result = await self.session.execute(stmt)
                model = result.unique().scalar_one_or_none()
                if model is None:
                    raise DatabaseException(
                        f"Failed to update promotion {promotion.id}: not found"
                    )

                model.name = promotion.name
                model.description = promotion.description
                model.promotion_type = str(promotion.promotion_type.value)
                model.rule = promotion.rule
                model.start_date = promotion.start_date
                model.end_date = promotion.end_date
                model.is_active = promotion.is_active
                model.max_uses = promotion.max_uses
                model.current_uses = promotion.current_uses
                model.created_at = promotion.created_at
                model.updated_at = promotion.updated_at

                if promotion.applicable_product_ids:
                    product_ids_values = [
                        p_id.value for p_id in promotion.applicable_product_ids
                    ]
                    products_stmt = select(ProductModel).where(
                        ProductModel.id.in_(product_ids_values)
                    )
                    products_result = await self.session.execute(products_stmt)
                    model.products = list(products_result.scalars().all())
                else:
                    model.products = []

                if promotion.applicable_categories_ids:
                    cat_stmt = select(ProductCategoryModel).where(
                        ProductCategoryModel.id.in_(
                            promotion.applicable_categories_ids
                        )
                    )
                    cat_result = await self.session.execute(cat_stmt)
                    model.categories = list(cat_result.scalars().all())
                else:
                    model.categories = []

                await self.session.commit()

                return promotion_model_to_domain(model)
        except SQLAlchemyError as e:
            logger.error(f"Error updating promotion {promotion.id}: {e}")
            raise DatabaseException(f"Failed to update promotion {promotion.id}") from e

    async def delete(self, promotion_id: PromotionId) -> bool:
        try:
            async with self.session.begin_nested():
                stmt = delete(PromotionModel).where(
                    PromotionModel.id == str(promotion_id.value)
                )
                result = await self.session.execute(stmt)
                if result.rowcount == 0:
                    logger.warning(f"No promotion found with ID {promotion_id}")
                    await self.session.rollback()
                    return False

                await self.session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting promotion {promotion_id}: {e}")
            await self.session.rollback()
            raise DatabaseException(f"Failed to delete promotion {promotion_id}") from e

    async def apply_promotion_use(self, promotion_id: PromotionId) -> bool:
        try:
            async with self.session.begin_nested():
                stmt = (
                    update(PromotionModel)
                    .where(PromotionModel.id == str(promotion_id.value))
                    .values(current_uses=PromotionModel.current_uses + 1)
                )
                result = await self.session.execute(stmt)
                return result.rowcount > 0
        except SQLAlchemyError as e:
            logger.error(f"Error applying promotion use {promotion_id}: {e}")
            raise DatabaseException(
                f"Failed to apply promotion use {promotion_id}"
            ) from e

    async def update_products(
        self, promotion_id: PromotionId, product_ids: List[ProductId]
    ) -> None:
        """Updates the products associated with a promotion"""
        try:
            async with self.session.begin_nested():
                stmt = select(PromotionModel).where(
                    and_(
                        PromotionModel.id == str(promotion_id.value),
                        PromotionModel.is_active == True,
                    )
                )
                result = await self.session.execute(stmt)
                model = result.unique().scalar_one_or_none()

                # Clear existing products
                stmt = delete(PromotionProductModel).where(
                    PromotionProductModel.promotion_id == str(promotion_id.value)
                )
                await self.session.execute(stmt)

                # Fetch new product models
                product_ids_values = [p_id.value for p_id in product_ids]
                for product_id in product_ids_values:
                    self.session.add(
                        PromotionProductModel(
                            promotion_id=promotion_id.value, product_id=product_id
                        )
                    )
                await self.session.flush()
                await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error updating products for promotion {promotion_id}: {e}")
            raise DatabaseException(
                f"Failed to update products for promotion {promotion_id}"
            ) from e

    async def update_categories(
        self, promotion_id: PromotionId, category_ids: List[int]
    ) -> None:
        try:
            async with self.session.begin_nested():
                stmt = select(PromotionModel).where(
                    and_(
                        PromotionModel.id == str(promotion_id.value),
                        PromotionModel.is_active == True,
                    )
                )
                result = await self.session.execute(stmt)
                model = result.unique().scalar_one_or_none()

                # Clear
                stmt = delete(PromotionCategoryModel).where(
                    PromotionCategoryModel.promotion_id == str(promotion_id.value)
                )
                await self.session.execute(stmt)

                # Fetch new product models
                category_ids_values = [c_id for c_id in category_ids]
                for category_id in category_ids_values:
                    self.session.add(
                        PromotionCategoryModel(
                            promotion_id=promotion_id.value, category_id=category_id
                        )
                    )

                await self.session.flush()
                await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error updating categories for promotion {promotion_id}: {e}")
            raise DatabaseException(
                f"Failed to update categories for promotion {promotion_id}",
            ) from e

    async def return_pageble_entities(
        self, where_clause, query: PaginationQuery, result
    ) -> Page[Promotion]:
        pagination_metadata = await self.get_pagination_metadata(where_clause, query)
        promotions = [
            promotion_model_to_domain(model)
            for model in result.scalars().unique().all()
            if model
        ]
        return Page(items=promotions, metadata=pagination_metadata)

    async def get_pagination_metadata(
        self,
        where_clause,
        page_params: PaginationQuery,
    ) -> PaginationMetadata:
        count_stmt = select(func.count(PromotionModel.id.distinct())).select_from(
            PromotionModel
        )

        count_stmt = count_stmt.where(where_clause)
        total_items = (await self.session.execute(count_stmt)).scalar_one()

        return PaginationMetadata.get_search_pagination_metadata(
            page_data=page_params, total_items=total_items
        )
