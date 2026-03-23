from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.products.domain.repositories import ProductCategoryRepository
from app.products.domain.entities.product_category import ProductCategory
from ..models.product_models import ProductCategoryModel
from .mapper import ModelMapper


class SQLAlchemyCategoryRepository(ProductCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, category_id: int) -> Optional[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        return ModelMapper.to_category_domain(model) if model else None

    async def find_all(self) -> List[ProductCategory]:
        stmt = select(ProductCategoryModel)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()

        return [category.to_domain() for category in categories]

    async def save(self, category: ProductCategory) -> ProductCategory:
        if not category.id:
            return await self._create(category)
        else:
            return await self._update(category)

    async def delete(self, category_id: int) -> bool:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id
        )
        result = await self.session.execute(stmt)
        category_model = result.scalars().first()

        if not category_model:
            return False

        await self.session.delete(category_model)
        await self.session.flush()
        return True

    async def exists_by_id(self, category_id: int) -> bool:
        stmt = select(ProductCategoryModel.id).where(
            ProductCategoryModel.id == category_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def exists_by_name(self, category_name: str) -> bool:
        stmt = select(ProductCategoryModel.id).where(
            ProductCategoryModel.name == category_name
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def _create(self, category: ProductCategory) -> ProductCategory:
        model = ProductCategoryModel(
            name=category.name,
            description=category.description or "",
            is_active=category.is_active,
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return model.to_domain()

    async def _update(self, category: ProductCategory) -> ProductCategory:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category.id
        )
        result = await self.session.execute(stmt)
        category_model = result.scalars().first()

        if not category_model:
            raise ValueError("Category not found")

        category_model.name = category.name
        category_model.description = category.description or ""
        category_model.is_active = category.is_active

        await self.session.flush()
        await self.session.commit()

        return ModelMapper.to_category_domain(category_model)

    async def find_deleted_by_id(self, category_id: int) -> Optional[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
            ProductCategoryModel.is_active.is_(False),
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return ModelMapper.to_category_domain(model) if model else None
