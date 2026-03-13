from typing import Any, Optional, Dict, List

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cinema.domain.entities import Cinema
from app.core.cinema.domain.repositories import CinemaRepository
from .models import CinemaModel
from .mappers import CinemaModelMapper as CinemaMapper


class SQLAlchemyCinemaRepository(CinemaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self, page_params: Dict[str, int]) -> List[Cinema]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 10)

        stmt = select(CinemaModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

    async def list_active(self) -> List[Cinema]:
        stmt = select(CinemaModel).where(CinemaModel.is_active == True)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

    async def search(
        self, page_params: Dict[str, int], filter_params: Dict[str, Any]
    ) -> List[Cinema]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 10)

        stmt = select(CinemaModel).offset(offset).limit(limit)

        if filter_params:
            filters = self._build_filters_param(filter_params)

            if filters:
                stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

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

    def _build_filters_param(self, filter_params: Dict[str, Any]) -> List[Any]:
        filters: List[Any] = []

        if "name" in filters:
            filters.append(CinemaModel.name.ilike(f"%{filter_params['name']}%"))
        if "tax_number" in filter_params:
            filters.append(CinemaModel.tax_number == filter_params["tax_number"])
        if "description" in filter_params:
            filters.append(
                CinemaModel.description.ilike(f"%{filter_params['description']}%")
            )

        if "is_active" in filter_params:
            filters.append(CinemaModel.is_active == filter_params["is_active"])
        if "has_parking" in filter_params:
            filters.append(CinemaModel.has_parking == filter_params["has_parking"])
        if "has_food_court" in filter_params:
            filters.append(
                CinemaModel.has_food_court == filter_params["has_food_court"]
            )

        if "type" in filter_params:
            filters.append(CinemaModel.type == filter_params["type"])
        if "status" in filter_params:
            filters.append(CinemaModel.status == filter_params["status"])
        if "region" in filter_params:
            filters.append(CinemaModel.region == filter_params["region"])

        if "min_screens" in filter_params:
            filters.append(CinemaModel.screens >= filter_params["min_screens"])
        if "max_screens" in filter_params:
            filters.append(CinemaModel.screens <= filter_params["max_screens"])

        if "renovated_after" in filter_params:
            filters.append(
                CinemaModel.last_renovation >= filter_params["renovated_after"]
            )
        if "renovated_before" in filter_params:
            filters.append(
                CinemaModel.last_renovation <= filter_params["renovated_before"]
            )

        if "latitude" in filter_params and "longitude" in filter_params:
            filters.append(CinemaModel.latitude == filter_params["latitude"])
            filters.append(CinemaModel.longitude == filter_params["longitude"])

        if "phone" in filter_params:
            filters.append(CinemaModel.phone == filter_params["phone"])
        if "email_contact" in filter_params:
            filters.append(
                CinemaModel.email_contact.ilike(f"%{filter_params['email_contact']}%")
            )

        return filters

    async def exists_by_id(self, entity_id: int) -> bool:
        stmt = select(CinemaModel).where(CinemaModel.id == entity_id)

        result = await self.session.execute(stmt)

        model = result.scalars().first()
        return model is not None
