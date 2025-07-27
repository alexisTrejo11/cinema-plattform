import math
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from typing import List, Optional, Tuple
from datetime import datetime
from app.promotions.domain.promotion import Promotion, PromotionId, ProductId
from ..model.promotion_model import PromotionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, and_, update
from sqlalchemy.exc import SQLAlchemyError
from app.products.infrastructure.persistence.db.sql.models import ProductModel
import logging
from app.shared.base_exceptions import DatabaseException
from app.promotions.app.queries.promotion_query import GetPromotionByProductIdQuery
from app.shared.pagination import PaginationMetadata, PaginationQuery

logger = logging.getLogger(__name__)


class SQLAlchemyPromotionRepository(PromotionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, promotion_id: PromotionId) -> Optional[Promotion]:
        try:
            stmt = select(PromotionModel).where(
                and_(
                    PromotionModel.id == str(promotion_id.value),
                    PromotionModel.is_active == True,
                )
            )
            result = await self.session.execute(stmt)
            model = result.unique().scalar_one_or_none()
            return model.to_domain() if model else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting promotion {promotion_id}: {e}")
            raise DatabaseException(f"Failed to get promotion {promotion_id}") from e

    async def get_active_promotions(
        self, query: PaginationQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        try:
            stmt = select(PromotionModel).where(
                and_(
                    PromotionModel.start_date <= datetime.now(),
                    PromotionModel.end_date >= datetime.now(),
                    PromotionModel.is_active == True,
                )
            )

            count_stmt = select(func.count()).select_from(ProductModel)

            if query.offset is not None and query.offset >= 0:
                stmt = stmt.offset(query.offset)
            if query.limit is not None and query.limit > 0:
                stmt = stmt.limit(query.limit)

            result = await self.session.execute(stmt)
            total_items = (await self.session.execute(count_stmt)).scalar_one()

            pagination_metadata = await self.get_search_pagination_metadata(
                query, total_items
            )

            promotions = [model.to_domain() for model in result.scalars().all()]
            return promotions, pagination_metadata
        except SQLAlchemyError as e:
            logger.error(f"Error getting active promotions: {e}")
            raise DatabaseException("Failed to get active promotions") from e

    async def get_by_product(
        self, query: GetPromotionByProductIdQuery
    ) -> Tuple[List[Promotion], PaginationMetadata]:
        try:
            stmt = (
                select(PromotionModel)
                .join(PromotionModel.products)
                .where(
                    and_(
                        ProductModel.id == str(query.product_id.value),
                        PromotionModel.is_active == True,
                        PromotionModel.start_date <= func.now(),
                        PromotionModel.end_date >= func.now(),
                    )
                )
            )

            count_stmt = select(func.count()).select_from(ProductModel)

            if query.pagination:
                if query.pagination.offset is not None and query.pagination.offset >= 0:
                    stmt = stmt.offset(query.pagination.offset)
                if query.pagination.limit is not None and query.pagination.limit > 0:
                    stmt = stmt.limit(query.pagination.limit)

            result = await self.session.execute(stmt)
            total_items = (await self.session.execute(count_stmt)).scalar_one()

            pagination_metadata = await self.get_search_pagination_metadata(
                query.pagination, total_items
            )

            promotions = [model.to_domain() for model in result.scalars().all()]
            return promotions, pagination_metadata
        except SQLAlchemyError as e:
            logger.error(
                f"Error getting promotions for product {query.product_id.to_string()}: {e}"
            )
            raise DatabaseException(
                f"Failed to get promotions for product {query.product_id.to_string()}"
            ) from e

    async def create(self, promotion: Promotion) -> Promotion:
        try:
            promotion_model = PromotionModel.from_domain(promotion)
            self.session.add(promotion_model)
            await self.session.flush()

            return promotion
        except SQLAlchemyError as e:
            logger.error(f"Error creating promotion: {e}")
            raise DatabaseException("Failed to create promotion") from e

    async def update(self, promotion: Promotion) -> Promotion:
        try:
            async with self.session.begin():
                promotion_model = PromotionModel.from_domain(promotion)
                promotion_model = await self.session.merge(promotion_model)
                await self.session.flush()
                return promotion_model.to_domain()
        except SQLAlchemyError as e:
            logger.error(f"Error updating promotion {promotion.id}: {e}")
            raise DatabaseException(f"Failed to update promotion {promotion.id}") from e

    async def delete(self, promotion_id: PromotionId) -> bool:
        try:
            async with self.session.begin():
                stmt = delete(PromotionModel).where(
                    PromotionModel.id == str(promotion_id.value)
                )
                result = await self.session.execute(stmt)
                return result.rowcount > 0
        except SQLAlchemyError as e:
            logger.error(f"Error deleting promotion {promotion_id}: {e}")
            raise DatabaseException(f"Failed to delete promotion {promotion_id}") from e

    async def apply_promotion_use(self, promotion_id: PromotionId) -> bool:
        try:
            async with self.session.begin():
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

    async def get_search_pagination_metadata(
        self, page_params: PaginationQuery, total_items: int
    ) -> PaginationMetadata:
        items_per_page = (
            page_params.limit
            if page_params.limit and page_params.limit > 0
            else total_items
        )
        current_page = (
            (page_params.offset // items_per_page) + 1
            if page_params.offset and items_per_page
            else 1
        )
        total_pages = (
            math.ceil(total_items / items_per_page) if items_per_page > 0 else 1
        )

        return PaginationMetadata(
            total_items=total_items,
            total_pages=total_pages,
            current_page=current_page,
            items_per_page=items_per_page,
        )
