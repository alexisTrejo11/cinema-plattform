from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.ticket.domain.entities.ticket import TicketStatus
from config.database import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False, index=True)
    showtime_id = Column(Integer, nullable=False, index=True)
    seat_number = Column(String(10), nullable=False)
    seat_type = Column(String(30), nullable=False, default='')
    price = Column(Float, nullable=False)
    status = Column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.RESERVED)
    reservation_time = Column(DateTime(timezone=True), server_default=func.now())
    confirmation_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
