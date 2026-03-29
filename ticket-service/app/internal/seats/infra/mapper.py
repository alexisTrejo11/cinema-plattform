from app.internal.seats.domain.showtime_seat import ShowtimeSeat

from .model import ShowtimeSeatModel


class ModelMapper:
    @staticmethod
    def to_domain(model: ShowtimeSeatModel) -> ShowtimeSeat:
        return ShowtimeSeat(
            id=model.id,
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
            showtime_id=domain.showtime_id,
            seat_id=domain.seat_id,
            seat_name=domain.seat_name,
            is_available=domain.is_available,
            created_at=domain.created_at,
            taken_at=domain.taken_at,
            ticket_id=domain.ticket_id,
            id=domain.id,
        )
