from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
from config.postgres_config import Base

class ShowtimeSeatModel(Base):
    __tablename__ = "showtime_seats"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, nullable=False)
    seat_id = Column(Integer, nullable=False) 
    seat_name = Column(String(10), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    taken_at = Column(DateTime, nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    ticket = relationship("Ticket", back_populates="showtime_seat", uselist=False) 

    def __repr__(self):
        return (f"<ShowtimeSeat(id={self.id}, showtime_id={self.showtime_id}, "
                f"seat_name='{self.seat_name}', is_available={self.is_available})>")