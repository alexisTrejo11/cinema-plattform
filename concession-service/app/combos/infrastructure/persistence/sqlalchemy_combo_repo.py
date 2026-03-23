from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload

from app.combos.domain.repository import ComboRepository
from app.combos.domain.entities.combo import Combo
from app.combos.domain.entities.value_objects import ComboId
from app.shared.pagination import PaginationQuery, Page, PaginationMetadata
from .models import ComboModel, ComboItemModel
from .model_mapper import combo_model_to_domain
from app.products.domain.entities.value_objects import ProductId


class SQLAlchemyComboRepository(ComboRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(
        self, combo_id: ComboId, include_items: bool
    ) -> Optional[Combo]:
        stmt = select(ComboModel).where(
            ComboModel.id == combo_id.value,
            ComboModel.is_available == True,
        )

        stmt = stmt.options(selectinload(ComboModel.items))

        result = await self.session.execute(stmt)

        combo_model = result.scalar_one_or_none()
        if not combo_model:
            return None

        return combo_model_to_domain(
            combo_model,
            True,  # Always include items when finding by ID
        )

    async def find_by_product(
        self,
        product_id: ProductId,
        pagination: PaginationQuery,
        include_items: bool = False,
    ) -> Page[Combo]:
        base = (
            select(ComboModel)
            .join(ComboItemModel, ComboItemModel.combo_id == ComboModel.id)
            .where(
                ComboItemModel.product_id == product_id.value,
                ComboModel.is_available.is_(True),
            )
            .distinct()
        )
        stmt = base
        if include_items:
            stmt = stmt.options(selectinload(ComboModel.items))
        stmt = PaginationQuery.paginate_stmt(stmt, pagination)

        result = await self.session.execute(stmt)

        count_stmt = select(func.count()).select_from(
            select(ComboModel.id)
            .join(ComboItemModel, ComboItemModel.combo_id == ComboModel.id)
            .where(
                ComboItemModel.product_id == product_id.value,
                ComboModel.is_available.is_(True),
            )
            .distinct()
            .subquery()
        )
        total_items = (await self.session.execute(count_stmt)).scalar_one()

        pagination_metadata = PaginationMetadata.get_search_pagination_metadata(
            pagination, total_items
        )

        return Page[Combo](
            [
                combo_model_to_domain(combo, include_items)
                for combo in result.scalars().unique().all()
            ],
            pagination_metadata,
        )

    async def find_active(self, pagination: PaginationQuery) -> Page[Combo]:
        stmt = select(ComboModel).where(ComboModel.is_available == True)
        stmt = PaginationQuery.paginate_stmt(stmt, pagination)

        stmt = stmt.options(selectinload(ComboModel.items))

        result = await self.session.execute(stmt)
        combo_models = result.scalars().unique().all()

        count_stmt = (
            select(func.count())
            .select_from(ComboModel)
            .where(ComboModel.is_available == True)
        )
        total_items = (await self.session.execute(count_stmt)).scalar_one()

        pagination_metadata = PaginationMetadata.get_search_pagination_metadata(
            pagination, total_items
        )

        combos = [combo_model_to_domain(combo, True) for combo in combo_models]
        return Page[Combo](combos, pagination_metadata)

    async def find_deleted_by_id(self, combo_id: ComboId) -> Optional[Combo]:
        stmt = select(ComboModel).where(
            ComboModel.id == combo_id.value,
            ComboModel.is_available.is_(False),
        )
        result = await self.session.execute(stmt)
        combo_model = result.scalar_one_or_none()
        return combo_model_to_domain(combo_model, False) if combo_model else None

    async def save(self, combo: Combo) -> None:
        select_stmt = select(ComboModel).where(ComboModel.id == combo.id.value)
        result = await self.session.execute(select_stmt)
        existing_combo = result.scalar_one_or_none()

        if existing_combo is None:
            combo_model = await self._create(combo)
        else:
            combo_model = await self._update(combo, existing_combo)
            delete_stmt = delete(ComboItemModel).where(
                ComboItemModel.combo_id == combo_model.id
            )
            await self.session.execute(delete_stmt)

        self._add_items(combo, combo_model)
        await self.session.commit()

    async def delete(self, combo_id: ComboId, soft_delete: bool = True) -> None:
        if soft_delete:
            await self._soft_delete(combo_id)
        else:
            await self._hard_delete(combo_id)

    def _add_items(self, combo: Combo, combo_model: ComboModel) -> None:
        for item in combo.items:
            item_model = ComboItemModel(
                id=item.id.value,
                combo_id=combo_model.id,
                product_id=item.product.id.value,
                quantity=item.quantity,
            )
            self.session.add(item_model)

    async def _update(self, combo: Combo, existing_combo: ComboModel) -> ComboModel:
        existing_combo.name = combo.name
        existing_combo.description = combo.description
        existing_combo.price = combo.price
        existing_combo.discount_percentage = combo.discount_percentage
        existing_combo.image_url = combo.image_url
        existing_combo.is_available = combo.is_available

        await self.session.merge(existing_combo)
        return existing_combo

    async def _create(self, combo: Combo) -> ComboModel:
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
        return combo_model

    async def _soft_delete(self, combo_id: ComboId) -> None:
        stmt = select(ComboModel).where(ComboModel.id == combo_id.value)
        result = await self.session.execute(stmt)
        combo = result.scalar_one_or_none()
        if combo:
            combo.is_available = False
            self.session.add(combo)
            await self.session.commit()

    async def _hard_delete(self, combo_id: ComboId) -> None:
        stmt = delete(ComboModel).where(ComboModel.id == combo_id.value)
        result = await self.session.execute(stmt)

        if not result.scalar_one_or_none():
            raise ValueError(f"Combo with ID {combo_id.value} does not exist.")

        await self.session.commit()

    async def get_items(self, model: ComboItemModel) -> List[ComboItemModel]:
        stmt = select(ComboItemModel).where(ComboItemModel.id == model.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
