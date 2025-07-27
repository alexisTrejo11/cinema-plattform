import math
from typing import Dict, Optional, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, and_

from app.products.domain.repositories import ProductRepository
from app.products.domain.entities.product import Product, ProductId
from app.products.application.queries import SearchProductsQuery
from ..sql.models import ProductModel
from app.shared.cache import cache
from app.shared.pagination import PaginationMetadata


class SqlAlchemyProductRepository(ProductRepository):
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

        if search_params.offset is not None and search_params.offset >= 0:
            stmt = stmt.offset(search_params.offset)
        if search_params.limit is not None and search_params.limit > 0:
            stmt = stmt.limit(search_params.limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        total_items = (await self.session.execute(count_stmt)).scalar_one()
        pagination_metadata = await self.get_search_pagination_metadata(
            search_params, total_items
        )

        return [model.to_domain() for model in models], pagination_metadata

    async def save(self, product: Product) -> Product:
        product_dict = product.to_dict()

        stmt = select(ProductModel).where(ProductModel.id == str(product.id.value))
        result = await self.session.execute(stmt)
        existing_model = result.scalar_one_or_none()

        if existing_model:
            for key, value in product_dict.items():
                setattr(existing_model, key, value)
            model = existing_model
        else:
            model = ProductModel(**product_dict)
            self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()

    async def delete(self, product_id: ProductId) -> None:
        stmt = delete(ProductModel).where(ProductModel.id == str(product_id.value))
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_search_pagination_metadata(
        self, search_params: SearchProductsQuery, total_items: int
    ) -> PaginationMetadata:
        items_per_page = (
            search_params.limit
            if search_params.limit and search_params.limit > 0
            else total_items
        )
        current_page = (
            (search_params.offset // items_per_page) + 1
            if search_params.offset and items_per_page
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
