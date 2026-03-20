from sqlalchemy.orm import Session
from config.db.postgres_config import get_db
from fastapi import Depends
from app.combos.domain.repository import ComboRepository
from app.products.domain.repositories import ProductRepository
from app.combos.application.use_cases.container import ComboUseCases
from sqlalchemy.ext.asyncio import AsyncSession


from app.combos.infrastructure.persistence.sqlalchemy_combo_repo import (
    SQLAlchemyComboRepository,
)
from app.products.infrastructure.persistence.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepository,
)


def get_combo_repository(session: AsyncSession = Depends(get_db)) -> ComboRepository:
    return SQLAlchemyComboRepository(session)


def get_product_repository(
    session: AsyncSession = Depends(get_db),
) -> ProductRepository:
    return SQLAlchemyProductRepository(session)


# Combo Use Cases
def get_combos_uc(
    combo_repo: ComboRepository = Depends(get_combo_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
) -> ComboUseCases:
    return ComboUseCases(combo_repo, product_repo)
