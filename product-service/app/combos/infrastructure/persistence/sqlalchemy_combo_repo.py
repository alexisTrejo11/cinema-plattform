from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, func
from sqlalchemy.orm import selectinload

from app.combos.domain.repository import ComboRepository
from app.combos.domain.entities.combo import Combo
from .models import ComboModel, ComboItemModel
from app.combos.domain.entities.value_objects import ComboId
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import PaginationQuery, Page, PaginationMetadata
from .model_mapper import ModelMapper


class SQLAlchemyComboRepository(ComboRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, query: GetComboByIdQuery) -> Optional[Combo]:
        stmt = select(ComboModel).where(
            ComboModel.id == query.combo_id.value,
            ComboModel.is_available == True,
        )

        if query.include_items:
            stmt = stmt.options(selectinload(ComboModel.items))

        result = await self.session.execute(stmt)
        combo_model = result.scalar_one_or_none()

        return (
            ModelMapper.to_domain(
                combo_model,
                query.include_items if query.include_items else False,
            )
            if combo_model
            else None
        )

    async def list_by_product(self, query: GetCombosByProductIdQuery) -> Page[Combo]:
        stmt = select(ComboModel).where(
            and_(
                ComboItemModel.product_id == query.product_id.value,
                ComboModel.is_available == True,
            )
        )

        if query.include_items:
            stmt = stmt.options(selectinload(ComboModel.items))

        result = await self.session.execute(stmt)

        count_stmt = (
            select(func.count())
            .select_from(ComboModel)
            .where(ComboModel.is_available == True)
        )
        total_items = (await self.session.execute(count_stmt)).scalar_one()

        pagination_metadata = PaginationMetadata.get_search_pagination_metadata(
            query.pagination, total_items
        )

        return Page(
            [
                ModelMapper.to_domain(
                    combo,
                    query.include_items if query.include_items else False,
                )
                for combo in result.scalars().all()
            ],
            pagination_metadata,
        )

    async def list_active(
        self, pagination: PaginationQuery, include_items: bool
    ) -> Page[Combo]:
        stmt = select(ComboModel).where(ComboModel.is_available == True)
        if include_items:
            stmt = stmt.options(selectinload(ComboModel.items))

        stmt = PaginationQuery.paginate_stmt(stmt, pagination)

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

        combos = [ModelMapper.to_domain(combo, True) for combo in combo_models]
        return Page(combos, pagination_metadata)

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

        if result.rowcount == 0:
            raise ValueError(f"Combo with ID {combo_id.value} does not exist.")

        await self.session.commit()

    async def get_items(self, model: ComboItemModel) -> List[ComboItemModel]:
        stmt = select(ComboItemModel).where(ComboItemModel.id == model.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
