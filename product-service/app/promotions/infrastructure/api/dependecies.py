from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db
from app.promotions.domain.repository.promotion_repository import PromotionRepository
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository,
)
from app.promotions.app.usecase.promotions_usecases import PromotionsUseCases
from app.products.infrastructure.api.depedencies import (
    get_food_repository,
    ProductRepository,
)


def get_promotion_repository(
    session: AsyncSession = Depends(get_db),
) -> PromotionRepository:
    return SQLAlchemyPromotionRepository(session)


def get_promotion_use_cases(
    repository: PromotionRepository = Depends(get_promotion_repository),
    product_repo: ProductRepository = Depends(get_food_repository),
) -> PromotionsUseCases:
    return PromotionsUseCases(repository, product_repo)
