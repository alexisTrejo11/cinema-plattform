from app.products.domain.repositories import ProductCategoryRepository
from app.products.domain.entities.product_category import ProductCategory
from typing import Optional, List
from .models import ProductCategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload


class SQLAlchemyCategoryRepository(ProductCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, category_id: int) -> Optional[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
            ProductCategoryModel.is_active == True,
        )
        result = await self.session.execute(stmt)
        category_model = result.scalars().first()

        return category_model.to_domain() if category_model else None

    async def list(self) -> List[ProductCategory]:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.is_active == True
        )
        result = await self.session.execute(stmt)
        categories = result.scalars().all()

        return [category.to_domain() for category in categories]

    async def save(self, category: ProductCategory) -> ProductCategory:
        category_dict = category.to_dict()
        if category.id == 0:
            # Create new category
            category_dict.pop("id", None)
            model = ProductCategoryModel(**category_dict)
            self.session.add(model)
            await self.session.flush()
        else:
            # Update existing category
            stmt = select(ProductCategoryModel).where(
                ProductCategoryModel.id == category.id
            )
            result = await self.session.execute(stmt)
            model = result.scalars().first()

            if model:
                for key, value in category_dict.items():
                    setattr(model, key, value)
            else:
                model = ProductCategoryModel(**category_dict)
                self.session.add(model)

            await self.session.flush()

        await self.session.refresh(model)
        return model.to_domain()

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
