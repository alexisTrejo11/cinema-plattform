from decimal import Decimal
from typing import List, Optional

from sqlalchemy import inspect as sa_inspect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.internal.seats.infra.mapper import ModelMapper as SeatModelMapper
from app.internal.ticket.application.dtos import SearchTicketParams
from app.internal.ticket.application.repository import TicketRepository
from app.internal.ticket.domain.entities.ticket import Ticket
from app.internal.ticket.domain.valueobjects.enums import TicketStatus, TicketType
from app.internal.ticket.domain.valueobjects.helping_classes import (
    CustomerDetails,
    PaymentDetails,
    PriceDetails,
)

from ..models.ticket_model import TicketModel


class SQLAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, search_params: SearchTicketParams) -> List[Ticket]:
        stmt = select(TicketModel)
        
        if search_params.movie_id:
            stmt = stmt.where(TicketModel.movie_id == search_params.movie_id)
        if search_params.showtime_id:
            stmt = stmt.where(TicketModel.showtime_id == search_params.showtime_id)
        if search_params.user_id:
            stmt = stmt.where(TicketModel.user_id == search_params.user_id)
        if search_params.status:
            stmt = stmt.where(TicketModel.status == search_params.status.value)
        if search_params.created_before:
            stmt = stmt.where(TicketModel.created_at <= search_params.created_before)
        if search_params.created_after:
            stmt = stmt.where(TicketModel.created_at >= search_params.created_after)
        if search_params.price_min is not None:
            stmt = stmt.where(TicketModel.price >= Decimal(str(search_params.price_min)))
        if search_params.price_max is not None:
            stmt = stmt.where(TicketModel.price <= Decimal(str(search_params.price_max)))
           
        sort_column = {
            "created_at": TicketModel.created_at,
            "updated_at": TicketModel.updated_at,
            "price": TicketModel.price
        }.get(search_params.sort_by, TicketModel.created_at)
        
        if search_params.sort_direction_asc:
            stmt = stmt.order_by(sort_column.asc())
        else:
            stmt = stmt.order_by(sort_column.desc())
        
        
        stmt = stmt.limit(search_params.page_limit).offset(search_params.page_offset)
        
        
        if search_params.include_seats:
            stmt = stmt.options(joinedload(TicketModel.showtime_seats))
        
        result = await self.session.execute(stmt)
        models = result.unique().scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def save(self, ticket: Ticket) -> Ticket:
        if not ticket.id:
            model = self._entity_to_model(ticket)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_entity(model)
        else:
            stmt = select(TicketModel).where(TicketModel.id == ticket.id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                raise ValueError(f"Ticket with ID {ticket.id} not found")

            self._update_model_from_entity(model, ticket)
            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_entity(model)
            
    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        stmt = (
            select(TicketModel)
            .where(TicketModel.id == ticket_id)
            .options(joinedload(TicketModel.showtime_seats))
        )

        result = await self.session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def list_by_user_id(self, user_id: int) -> List[Ticket]:
        stmt = select(TicketModel).where(TicketModel.user_id == user_id)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()       
        
        return [self._model_to_entity(model) for model in models]

    async def list_by_showtime_id(self, showtime_id: int) -> List[Ticket]:
        stmt = select(TicketModel).where(TicketModel.showtime_id == showtime_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]        

    async def delete(self, ticket_id: int) -> bool:
        stmt_select = select(TicketModel).where(TicketModel.id == ticket_id)
        result = await self.session.execute(stmt_select)
        model = result.scalar_one_or_none()

        if not model:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    
    def _model_to_entity(self, model: TicketModel) -> Ticket:
        price_details = PriceDetails(price=model.price, currency=model.price_currency)
        customer_details = None
        if model.customer_email or model.user_id is not None:
            customer_details = CustomerDetails(
                user_email=model.customer_email or "",
                id=model.user_id,
                customer_ip_address=model.customer_ip,
            )
        payment_details = None
        if model.payment_id is not None and model.transaction_id is not None:
            payment_details = PaymentDetails(
                id=model.payment_id,
                transaction_id=model.transaction_id,
                type="movie-ticket",
                method="digital",
                currency=model.price_currency,
            )
        seats = []
        state = sa_inspect(model)
        if "showtime_seats" not in state.unloaded:
            raw_seats = model.showtime_seats or []
            seats = [SeatModelMapper.to_domain(m) for m in raw_seats]
        return Ticket(
            id=model.id,
            showtime_id=model.showtime_id,
            movie_id=model.movie_id,
            price_details=price_details,
            payment_details=payment_details,
            ticket_type=TicketType(model.ticket_type),
            status=TicketStatus(model.status),
            customer_details=customer_details,
            seats=seats,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model(self, entity: Ticket) -> TicketModel:
        model = TicketModel(
            id=entity.id,
            showtime_id=entity.showtime_id,
            price=entity.price_details.price,
            movie_id=entity.movie_id,
            price_currency=entity.price_details.currency,
            ticket_type=entity.ticket_type.value,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
        if entity.customer_details:
            model.customer_email = entity.customer_details.user_email
            model.user_id = entity.customer_details.id if entity.customer_details.id else None
            model.customer_ip = entity.customer_details.customer_ip_address
        if entity.payment_details:
            model.payment_id = entity.payment_details.id
            model.transaction_id = entity.payment_details.transaction_id

        return model

    def _update_model_from_entity(self, model: TicketModel, entity: Ticket) -> None:
        """Update an existing model instance with values from the entity"""
        model.showtime_id = entity.showtime_id
        model.movie_id = entity.movie_id
        model.price = entity.price_details.price
        model.price_currency = entity.price_details.currency
        model.ticket_type = entity.ticket_type.value
        model.status = entity.status.value
        model.updated_at = entity.updated_at

        if entity.customer_details:
            model.customer_email = entity.customer_details.user_email
            model.user_id = entity.customer_details.id if entity.customer_details.id else None
            model.customer_ip = entity.customer_details.customer_ip_address
        if entity.payment_details:
            model.payment_id = entity.payment_details.id
            model.transaction_id = entity.payment_details.transaction_id
