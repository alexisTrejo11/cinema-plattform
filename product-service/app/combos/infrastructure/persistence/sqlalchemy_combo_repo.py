from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import joinedload
from sqlalchemy import inspect
from app.combos.domain.repository import ComboRepository
from app.combos.domain.entities.combo import Combo, ComboItem
from .models import ComboModel, ComboItemModel
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import PaginationQuery


class SqlAlchemyComboRepository(ComboRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, search_query: GetComboByIdQuery) -> Optional[Combo]:
        stmt = select(ComboModel).where(ComboModel.id == search_query.combo_id.value)

        if search_query.include_items:
            stmt = stmt.options(
                joinedload(ComboModel.items).joinedload(ComboItemModel.product)
            )
        result = await self.session.execute(stmt)
        if search_query.include_items:
            combo_model = result.unique().scalar_one_or_none()
        else:
            combo_model = result.scalar_one_or_none()

        if not combo_model:
            return None

        return self._to_domain(
            combo_model,
            search_query.include_items if search_query.include_items else False,
        )

    async def list_by_product(
        self, search_query: GetCombosByProductIdQuery
    ) -> List[Combo]:
        stmt = (
            select(ComboModel)
            .join(ComboItemModel)
            .where(
                and_(
                    ComboItemModel.product_id == search_query.product_id.value,
                    ComboModel.is_available == True,
                )
            )
        )

        if search_query.include_items:
            stmt = stmt.options(
                joinedload(ComboModel.items).joinedload(ComboItemModel.product)
            )

        result = await self.session.execute(stmt)
        if search_query.include_items:
            combo_models = result.scalars().unique().all()
        else:
            combo_models = result.scalars().all()

        return [
            self._to_domain(
                combo,
                search_query.include_items if search_query.include_items else False,
            )
            for combo in combo_models
        ]

    async def list(self, pagination: PaginationQuery) -> List[Combo]:
        stmt = select(ComboModel).options(
            joinedload(ComboModel.items).joinedload(ComboItemModel.product)
        )

        if pagination.limit:
            stmt = stmt.limit(pagination.limit)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)

        result = await self.session.execute(stmt)
        combo_models = result.scalars().unique().all()

        return [self._to_domain(combo, True) for combo in combo_models]

    async def save(self, combo: Combo) -> Combo:
        select_stmt = select(ComboModel).where(ComboModel.id == combo.id.value)
        result = await self.session.execute(select_stmt)
        existing_combo = result.scalar_one_or_none()
        
        if existing_combo is None:
            # Create new combo
            combo_model = ComboModel(
                id=combo.id.value,
                name=combo.name,
                description=combo.description,
                price=combo.price,
                discount_percentage=combo.discount_percentage,
                image_url=combo.image_url,
                is_available=combo.is_available,
            )
            self.session.add(combo_model)
            await self.session.flush()  # Get the ID
        else:
            # Update existing combo
            combo_model = existing_combo
            combo_model.name = combo.name
            combo_model.description = combo.description
            combo_model.price = combo.price
            combo_model.discount_percentage = combo.discount_percentage
            combo_model.image_url = combo.image_url
            combo_model.is_available = combo.is_available

            # Delete existing items
            await self.session.execute(
                delete(ComboItemModel).where(ComboItemModel.combo_id == combo.id.value)
            )

        # Add items
        for item in combo.items:
            item_model = ComboItemModel(
                id=item.id.value,
                combo_id=combo_model.id,  # Use combo_id instead of combo object
                product_id=item.product.id.value,
                quantity=item.quantity,
            )
            self.session.add(item_model)

        await self.session.commit()
        
        # Re-fetch with proper eager loading to avoid lazy loading issues
        stmt = select(ComboModel).where(ComboModel.id == combo.id.value).options(
            joinedload(ComboModel.items).joinedload(ComboItemModel.product)
        )
        result = await self.session.execute(stmt)
        combo_model_with_items = result.unique().scalar_one()
        
        return self._to_domain(combo_model_with_items, True)

    async def soft_delete(self, combo_id: ComboId) -> None:
        stmt = select(ComboModel).where(ComboModel.id == combo_id.value)
        result = await self.session.execute(stmt)
        combo = result.scalar_one_or_none()
        if combo:
            combo.is_available = False
            self.session.add(combo)
            await self.session.commit()

    def _to_domain(self, combo_model: ComboModel, include_items: bool) -> Combo:
        """Convert SQLAlchemy model to domain model"""
        items = []
        if include_items:
            # Check if items relationship is loaded to avoid lazy loading
            state = inspect(combo_model)
            if 'items' in state.unloaded:
                # Items aren't loaded, return empty list to avoid lazy loading
                pass  # items remains empty list
            else:
                # Items are loaded or being loaded, safe to access
                for item in combo_model.items:
                    items.append(
                        ComboItem(item.product.to_domain(), ComboItemId(item.id), item.quantity)
                    )

        return Combo(
            id=ComboId(combo_model.id),
            name=combo_model.name,
            description=combo_model.description,
            price=combo_model.price,
            discount_percentage=combo_model.discount_percentage,
            image_url=combo_model.image_url,
            is_available=combo_model.is_available,
            created_at=combo_model.created_at,
            updated_at=combo_model.updated_at,
            items=items,
        )
