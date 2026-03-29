from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from config.postgres_config import Base
from datetime import datetime

class ShowtimeSeatModel(Base):
    __tablename__ = "showtime_seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    showtime_id: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_id: Mapped[int] = mapped_column(Integer, nullable=False) 
    seat_name: Mapped[str] = mapped_column(String(10), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    taken_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("tickets.id"), nullable=True)
    ticket = relationship("TicketModel", back_populates="showtime_seats", uselist=False)

    def __repr__(self):
        return (f"<ShowtimeSeat(id={self.id}, showtime_id={self.showtime_id}, "
                f"seat_name='{self.seat_name}', is_available={self.is_available})>")