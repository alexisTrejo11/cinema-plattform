from pydantic import BaseModel

class Seats(BaseModel):
    seat_id: int
    seat_row: str
    seat_number: int
    is_taken: bool = False