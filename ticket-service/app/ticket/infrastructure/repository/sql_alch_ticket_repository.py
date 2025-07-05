from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, update, delete

from app.ticket.domain.entities.ticket import Ticket, TicketStatus, PriceDetails, CustomerDetails, TicketType
from app.ticket.application.repository import TicketRepository
from ..models.ticket_model import TicketModel

class SQLAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, **kwargs) -> List[Ticket]:
            return []
    
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

            # Update the existing model with new values
            self._update_model_from_entity(model, ticket)
            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_entity(model)
            
    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        stmt = select(TicketModel).where(TicketModel.id == ticket_id)
        
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()       
        
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
        price_details = PriceDetails(model.price, model.price_currency)
        customer_details = CustomerDetails(model.customer_email, model.user_id, model.customer_ip)
        return Ticket(
            id=model.id,
            showtime_id=model.showtime_id,
            movie_id=model.movie_id,
            price_details=price_details,
            ticket_type=TicketType(model.ticket_type),
            status=TicketStatus(model.status),
            customer_details=customer_details,
            created_at=model.created_at,
            updated_at=model.updated_at
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
