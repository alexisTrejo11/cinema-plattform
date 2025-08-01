import logging
import math
from typing import List, Optional, Tuple
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, and_, update
from sqlalchemy.exc import SQLAlchemyError

from app.shared.base_exceptions import DatabaseException
from app.shared.pagination import PaginationMetadata, PaginationQuery

from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.domain.promotion import Promotion, PromotionId, ProductId
from app.promotions.application.queries.promotion_query import (
    GetPromotionByProductIdQuery,
)
from app.products.infrastructure.persistence.models.product_models import (
    ProductModel,
)
from ..model.promotion_model import (
    PromotionModel,
    PromotionCategoryModel,
    PromotionProductModel,
)
from ..model.model_mapper import PromotionModelMapper

logger = logging.getLogger(__name__)


class SQLAlchemyPromotionRepository(PromotionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(
        self, promotion_id: PromotionId, is_active: Optional[bool] = True
    ) -> Optional[Promotion]:
        try:
            stmt = select(PromotionModel).where(
                and_(
                    PromotionModel.id == str(promotion_id.value),
                    PromotionModel.is_active == is_active,
                )
            )
            result = await self.session.execute(stmt)
            model = result.unique().scalar_one_or_none()
            return PromotionModelMapper.to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting promotion {promotion_id}: {e}")
            raise DatabaseException(f"Failed to get promotion {promotion_id}") from e

    async def get_active_promotions(
        self, query: PaginationQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        try:
            where_clause = and_(
                PromotionModel.start_date <= datetime.now(),
                PromotionModel.end_date >= datetime.now(),
                PromotionModel.is_active == True,
            )
            stmt = select(PromotionModel).where(where_clause)
            stmt = self.paginate_query(stmt, query)

            result = await self.session.execute(stmt)

            pagination_metadata = await self.get_pagination_metadata(
                where_clause, query
            )

            return self.return_pageble_entities(result, pagination_metadata)
        except SQLAlchemyError as e:
            logger.error(f"Error getting active promotions: {e}")
            raise DatabaseException("Failed to get active promotions") from e

    async def get_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        try:
            where_clause = and_(
                ProductModel.id == str(query.product_id.value),
                PromotionModel.is_active == True,
                PromotionModel.start_date <= func.now(),
                PromotionModel.end_date >= func.now(),
            )

            stmt = (
                select(PromotionModel).join(PromotionModel.products).where(where_clause)
            )

            if query.pagination:
                stmt = self.paginate_query(stmt, query.pagination)

            result = await self.session.execute(stmt)

            pagination_metadata = await self.get_pagination_metadata(
                where_clause, query.pagination, True
            )

            return self.return_pageble_entities(result, pagination_metadata)
        except SQLAlchemyError as e:
            logger.error(
                f"Error getting promotions for product {query.product_id.to_string()}: {e}"
            )
            raise DatabaseException(
                f"Failed to get promotions for product {query.product_id.to_string()}"
            ) from e

    async def create(self, promotion: Promotion) -> Promotion:
        try:
            promotion_model = PromotionModelMapper.from_domain(promotion)

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

            return PromotionModelMapper.to_domain(promotion_model)
        except SQLAlchemyError as e:
            logger.error(f"Error creating promotion: {e}")
            raise DatabaseException("Failed to create promotion") from e

    async def update(self, promotion: Promotion) -> Promotion:
        try:
            async with self.session.begin_nested():
                promotion_model = PromotionModelMapper.from_domain(promotion)

                promotion_model = await self.session.merge(promotion_model)
                await self.session.commit()

                return PromotionModelMapper.to_domain(promotion_model)
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
                f"Failed to update categories for promotion {promotion_id}"
            ) from e

    async def get_pagination_metadata(
        self,
        where_clause,
        page_params: PaginationQuery,
        apply_join_for_count: bool = False,  # New parameter
    ) -> PaginationMetadata:
        count_stmt = select(func.count(PromotionModel.id.distinct())).select_from(
            PromotionModel
        )

        if apply_join_for_count:
            # ONLY apply join if we are counting for get_by_product
            count_stmt = count_stmt.join(PromotionModel.products)

        count_stmt = count_stmt.where(where_clause)

        total_items = (await self.session.execute(count_stmt)).scalar_one()

        items_per_page = (
            page_params.page_size
            if page_params.page_size and page_params.page_size > 0
            else total_items
        )
        current_page = page_params.page

        total_pages = 1
        if total_items > 0 and items_per_page > 0:
            total_pages = math.ceil(total_items / items_per_page)

        return PaginationMetadata(
            total_items=total_items,
            total_pages=total_pages,
            current_page=current_page,
            items_per_page=items_per_page,
        )

    def paginate_query(self, stmt, page_params: PaginationQuery):
        if page_params.page is not None and page_params.page >= 0:
            stmt = stmt.offset((page_params.page - 1) * page_params.page_size)
        if page_params.page_size is not None and page_params.page_size > 0:
            stmt = stmt.limit(page_params.page_size)
        return stmt

    def return_pageble_entities(
        self, result, page_metadata: PaginationMetadata
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        promotions = [
            PromotionModelMapper.to_domain(model)
            for model in result.scalars().unique().all()
            if model
        ]
        return promotions, page_metadata
