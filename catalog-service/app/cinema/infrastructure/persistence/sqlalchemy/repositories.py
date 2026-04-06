from typing import Any, Optional, Dict, List

from sqlalchemy import and_, select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.cinema.domain.entities import Cinema
from app.cinema.domain.repositories import CinemaRepository
from app.cinema.application.dtos import SearchCinemaFilters
from app.shared.core.pagination import PaginationParams, Page
from .models import CinemaModel
from .mappers import CinemaModelMapper as CinemaMapper


class SQLAlchemyCinemaRepository(CinemaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self, page_params: Dict[str, int]) -> List[Cinema]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 10)

        stmt = select(CinemaModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

    async def find_active(self, params: PaginationParams) -> Page[Cinema]:
        # Count total active cinemas
        count_stmt = (
            select(func.count())
            .select_from(CinemaModel)
            .where(CinemaModel.is_active == True)
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        # Get paginated active cinemas
        stmt = select(CinemaModel).where(CinemaModel.is_active == True)
        stmt = stmt.offset(params.offset).limit(params.limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        cinemas = [CinemaMapper.to_domain(model) for model in models]
        return Page.create(items=cinemas, total=total, params=params)

    async def search(
        self, params: PaginationParams, filters: SearchCinemaFilters
    ) -> Page[Cinema]:
        # Build base query
        stmt = select(CinemaModel)
        count_stmt = select(func.count()).select_from(CinemaModel)

        # app. filters
        filter_conditions = self._build_filters_param(filters)
        if filter_conditions:
            stmt = stmt.where(and_(*filter_conditions))
            count_stmt = count_stmt.where(and_(*filter_conditions))

        # Get total count
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        # app. pagination
        stmt = stmt.offset(params.offset).limit(params.limit)

        # Execute query
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        cinemas = [CinemaMapper.to_domain(model) for model in models]
        return Page.create(items=cinemas, total=total, params=params)

    async def find_by_id(self, entity_id: int) -> Optional[Cinema]:
        model = await self.session.get(CinemaModel, entity_id)

        return CinemaMapper.to_domain(model) if model else None

    async def find_by_tax_number(self, tax_number: str) -> Optional[Cinema]:
        stmt = select(CinemaModel).where(CinemaModel.tax_number == tax_number)
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        return CinemaMapper.to_domain(model) if model else None

    async def save(self, entity: Cinema) -> Cinema:
        model = CinemaMapper.from_domain(entity)

        if entity.id is None:
            self.session.add(model)
        else:
            model = await self.session.merge(model)

        await self.session.commit()
        await self.session.refresh(model)

        return CinemaMapper.to_domain(model)

    async def delete(self, entity_id: int) -> None:
        stmt = delete(CinemaModel).where(CinemaModel.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()

    def _build_filters_param(self, filters: SearchCinemaFilters) -> List[Any]:
        conditions: List[Any] = []

        if filters.name:
            conditions.append(CinemaModel.name.ilike(f"%{filters.name}%"))
        if filters.tax_number:
            conditions.append(CinemaModel.tax_number == filters.tax_number)
        if filters.is_active is not None:
            conditions.append(CinemaModel.is_active == filters.is_active)
        if filters.has_parking is not None:
            conditions.append(CinemaModel.has_parking == filters.has_parking)
        if filters.has_food_court is not None:
            conditions.append(CinemaModel.has_food_court == filters.has_food_court)

        if filters.type:
            conditions.append(CinemaModel.type == filters.type)
        if filters.status:
            conditions.append(CinemaModel.status == filters.status)
        if filters.region:
            conditions.append(CinemaModel.region == filters.region)

        if filters.min_screens is not None:
            conditions.append(CinemaModel.screens >= filters.min_screens)
        if filters.max_screens is not None:
            conditions.append(CinemaModel.screens <= filters.max_screens)

        if filters.renovated_after:
            conditions.append(CinemaModel.last_renovation >= filters.renovated_after)
        if filters.renovated_before:
            conditions.append(CinemaModel.last_renovation <= filters.renovated_before)

        if filters.latitude is not None and filters.longitude is not None:
            conditions.append(CinemaModel.latitude == filters.latitude)
            conditions.append(CinemaModel.longitude == filters.longitude)

        if filters.phone:
            conditions.append(CinemaModel.phone == filters.phone)
        if filters.email_contact:
            conditions.append(
                CinemaModel.email_contact.ilike(f"%{filters.email_contact}%")
            )

        return conditions

    async def exists_by_id(self, entity_id: int) -> bool:
        stmt = select(CinemaModel).where(CinemaModel.id == entity_id)

        result = await self.session.execute(stmt)

        model = result.scalars().first()
        return model is not None

    async def is_deleted(self, entity_id: int) -> bool:
        stmt = select(CinemaModel).where(CinemaModel.id == entity_id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        return model is not None and model.deleted_at is not None

    async def count_active(self) -> int:
        stmt = (
            select(func.count())
            .select_from(CinemaModel)
            .where(CinemaModel.is_active == True)
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def restore(self, entity_id: int) -> None:
        stmt = (
            update(CinemaModel)
            .where(CinemaModel.id == entity_id)
            .values(deleted_at=None)
        )
        await self.session.execute(stmt)
        await self.session.commit()
