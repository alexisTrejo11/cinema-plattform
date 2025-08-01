from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.cache import cache, invalidate_cache
from app.products.domain.repositories import ProductCategoryRepository
from app.products.domain.entities.product_category import ProductCategory
from ..models.product_models import ProductCategoryModel
from .mapper import ModelMapper


class SQLAlchemyCategoryRepository(ProductCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @cache(key_template="product_category:{category_id}", ttl=60)
    async def get_by_id(self, category_id: int) -> Optional[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
            ProductCategoryModel.is_active == True,
        )
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        return ModelMapper.to_category_domain(model) if model else None

    async def list(self) -> List[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.is_active == True
        )
        result = await self.session.execute(stmt)
        categories = result.scalars().all()

        return [category.to_domain() for category in categories]

    @invalidate_cache(key_template="product_category:{category.id}")
    async def save(self, category: ProductCategory) -> ProductCategory:
        if not category.id:
            return await self._create(category)
        else:
            return await self._update(category)

    @invalidate_cache(key_template="product_category:{category_id}")
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
        model = ProductCategoryModel(**category.to_dict())

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

        for key, value in category.to_dict().items():
            setattr(category_model, key, value)

        await self.session.flush()
        await self.session.commit()

        return ModelMapper.to_category_domain(category_model)
