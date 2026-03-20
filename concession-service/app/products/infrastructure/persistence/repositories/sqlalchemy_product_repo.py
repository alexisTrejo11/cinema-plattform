from typing import Dict, Optional, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, and_

from app.shared.pagination import PaginationMetadata, PaginationQuery
from app.products.domain.repositories import ProductRepository
from app.products.domain.entities.product import Product, ProductId
from app.products.application.queries import SearchProductsQuery

from ..models.product_models import ProductModel
from .mapper import ModelMapper


class SQLAlchemyProductRepository(ProductRepository):
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

        return ModelMapper.to_domain(model) if model else None

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
        return {ProductId(model.id): ModelMapper.to_domain(model) for model in models}

    async def search(
        self, search_params: SearchProductsQuery
    ) -> Tuple[List[Product], PaginationMetadata]:
        stmt = select(ProductModel)

        conditions = []
        if search_params.min_price is not None:
            conditions.append(ProductModel.price >= search_params.min_price)
        if search_params.max_price is not None:
            conditions.append(ProductModel.price <= search_params.max_price)
        if search_params.name:
            conditions.append(ProductModel.name.ilike(f"%{search_params.name}%"))
        if search_params.category is not None:
            conditions.append(ProductModel.category_id == search_params.category)
        if search_params.active_only:
            conditions.append(ProductModel.is_available == True)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Ordenación
        stmt = stmt.order_by(ProductModel.name)

        count_stmt = select(func.count()).select_from(ProductModel)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))

        stmt = PaginationQuery.paginate_stmt(stmt, search_params.page)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        total_items = (await self.session.execute(count_stmt)).scalar_one()
        pagination_metadata = PaginationMetadata.get_search_pagination_metadata(
            search_params.page, total_items
        )

        return [ModelMapper.to_domain(model) for model in models], pagination_metadata

    async def save(self, product: Product) -> Product:
        model = ModelMapper.from_domain(product)
        stmt = select(ProductModel).where(ProductModel.id == product.id.value)
        result = await self.session.execute(stmt)
        existing_model = result.scalar_one_or_none()

        if existing_model:
            await self.session.merge(model)
        else:
            self.session.add(model)

        await self.session.commit()
        return ModelMapper.to_domain(model)

    async def delete(self, product_id: ProductId) -> None:
        stmt = delete(ProductModel).where(ProductModel.id == str(product_id.value))
        await self.session.execute(stmt)
        await self.session.commit()
