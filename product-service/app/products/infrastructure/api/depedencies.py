from sqlalchemy.orm import Session
from config.postgres_config import get_db
from fastapi import Depends
from app.products.domain.repositories import (
    ProductCategoryRepository,
    ProductRepository,
)
from app.products.application.usecases.container import (
    ProductUseCases,
    ProductCategoryUseCases,
)
from app.products.infrastructure.persistence.sqlachemy_category_repo import (
    SQLAlchemyCategoryRepository,
)
from app.products.infrastructure.persistence.sqlalchemy_product_repo import (
    SqlAlchProductRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession


# Repository dependencies
def get_category_repository(
    session: AsyncSession = Depends(get_db),
) -> ProductCategoryRepository:
    return SQLAlchemyCategoryRepository(session)


def get_food_repository(session: AsyncSession = Depends(get_db)) -> ProductRepository:
    return SqlAlchProductRepository(session)


# Category
def get_category_use_cases(
    category_repo: ProductCategoryRepository = Depends(get_category_repository),
) -> ProductCategoryUseCases:
    return ProductCategoryUseCases(category_repository=category_repo)


# Product
def get_product_use_cases(
    food_repo: ProductRepository = Depends(get_food_repository),
    category_repo: ProductCategoryRepository = Depends(get_category_repository),
) -> ProductUseCases:
    return ProductUseCases(
        product_repository=food_repo,
        category_repository=category_repo,
    )
