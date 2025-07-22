from app.products.domain.repositories import ProductRepository
from app.products.domain.entities.product import Product, ProductId
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from .models import ProductModel
from app.products.application.queries import SearchProductsQuery


class SqlAlchProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, product_id: ProductId) -> Optional[Product]:
        stmt = select(ProductModel).where(
            and_(
                ProductModel.id == str(product_id.value),
                ProductModel.is_available == True,
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def get_by_id_in(
        self, product_id_list: List[ProductId]
    ) -> Dict[ProductId, Product]:
        if not product_id_list:
            return {}

        stmt = select(ProductModel).where(
            and_(
                ProductModel.id.in_([str(p_id.value) for p_id in product_id_list]),
                ProductModel.is_available == True,
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return {ProductId(model.id): model.to_domain() for model in models}

    async def search(self, food_params: SearchProductsQuery) -> List[Product]:
        stmt = select(ProductModel)

        conditions = []
        if food_params.min_price is not None:
            conditions.append(ProductModel.price >= food_params.min_price)
        if food_params.max_price is not None:
            conditions.append(ProductModel.price <= food_params.max_price)
        if food_params.name:
            conditions.append(ProductModel.name.ilike(f"%{food_params.name}%"))
        if food_params.category is not None:
            conditions.append(ProductModel.category_id == food_params.category)
        if food_params.active_only:
            conditions.append(ProductModel.is_available == True)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(ProductModel.name)

        if food_params.offset is not None and food_params.offset >= 0:
            stmt = stmt.offset(food_params.offset)
        if food_params.limit is not None and food_params.limit > 0:
            stmt = stmt.limit(food_params.limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [model.to_domain() for model in models]

    async def save(self, product: Product) -> Product:
        product_dict = product.to_dict()
        
        # Check if product already exists in database
        stmt = select(ProductModel).where(ProductModel.id == str(product.id.value))
        result = await self.session.execute(stmt)
        existing_model = result.scalar_one_or_none()
        
        if existing_model:
            # Update existing product
            for key, value in product_dict.items():
                setattr(existing_model, key, value)
            model = existing_model
        else:
            # Create new product
            model = ProductModel(**product_dict)
            self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()

    async def delete(self, product_id: ProductId) -> None:
        stmt = delete(ProductModel).where(ProductModel.id == str(product_id.value))
        await self.session.execute(stmt)
        await self.session.commit()
