from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.ticket.domain.entities.ticket import Ticket, TicketStatus
from app.ticket.application.repositories import TicketRepository
from ..models.ticket_model import TicketModel

class SQLAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: Session):
        self.session = session

    async def save(self, ticket: Ticket) -> Ticket:
        if not ticket.id:
            model = self._entity_to_model(ticket)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        else:
            model = self.session.query(TicketModel).filter(TicketModel.id == ticket.id).first()
            if not model:
                raise ValueError("Ticket not found")

            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
            
    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        return self._model_to_entity(model) if model else None

    async def get_by_user_id(self, user_id: int) -> List[Ticket]:
        models = self.session.query(TicketModel).filter(TicketModel.user_id == user_id).all()
        return [self._model_to_entity(model) for model in models]

    async def get_by_showtime_id(self, showtime_id: int) -> List[Ticket]:
        models = self.session.query(TicketModel).filter(TicketModel.showtime_id == showtime_id).all()
        return [self._model_to_entity(model) for model in models]        

    async def delete(self, ticket_id: int) -> bool:
        model = self.session.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if not model:
            return False

        self.session.delete(model)
        self.session.commit()
        return True

    async def get_reserved_seats(self, showtime_id: int) -> List[str]:
        models = self.session.query(TicketModel).filter(
            and_(
                TicketModel.showtime_id == showtime_id,
                TicketModel.status.in_([TicketStatus.RESERVED, TicketStatus.CONFIRMED])
            )
        ).all()
        return [model.seat_number for model in models]

    async def get_by_status(self, status: TicketStatus) -> List[Ticket]:
        models = self.session.query(TicketModel).filter(TicketModel.status == status).all()
        return [self._model_to_entity(model) for model in models]
    
    
    def _model_to_entity(self, model: TicketModel) -> Ticket:
        """Convert SQLAlchemy model to domain entity"""
        return Ticket()

    def _entity_to_model(self, entity: Ticket) -> TicketModel:
        """Convert domain entity to SQLAlchemy model"""
        return TicketModel()