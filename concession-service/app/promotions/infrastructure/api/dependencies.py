from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db.postgres_config import get_db
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository,
)
from app.products.infrastructure.api.dependencies import (
    get_food_repository,
    ProductRepository,
    ProductCategoryRepository,
    get_category_repository,
)
from .container import PromotionsUseCasesContainer


def get_promotion_repository(
    session: AsyncSession = Depends(get_db),
) -> PromotionRepository:
    return SQLAlchemyPromotionRepository(session)


def get_promotion_use_cases(
    repository: PromotionRepository = Depends(get_promotion_repository),
    product_repo: ProductRepository = Depends(get_food_repository),
    category_repo: ProductCategoryRepository = Depends(get_category_repository),
) -> PromotionsUseCasesContainer:
    return PromotionsUseCasesContainer(repository, product_repo, category_repo)
