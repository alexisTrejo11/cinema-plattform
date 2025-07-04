from .model import ShowtimeSeatModel
from app.seats.domain.showtime_seat import ShowtimeSeat

class ModelMapper:
    @staticmethod
    def to_domain(model : ShowtimeSeatModel) -> ShowtimeSeat:
          return ShowtimeSeat(
            showtime_id=model.showtime_id,
            seat_id=model.seat_id,
            seat_name=model.seat_name,
            is_available=model.is_available,
            created_at=model.created_at,
            taken_at=model.taken_at,
            ticket_id=model.ticket_id,
        )
          
    @staticmethod
    def from_domain(domain: ShowtimeSeat) -> ShowtimeSeatModel:
        return ShowtimeSeatModel(
            showtime_id=domain.get_showtime_id(),
            seat_id=domain.get_seat_id(),
            seat_name=domain.get_seat_name(),
            is_available=domain.get_is_available(),
            created_at=domain.get_created_at(),
            taken_at=domain.get_taken_at(),
            ticket_id=domain.get_ticket_id(),
            id=domain.get_id()
        )