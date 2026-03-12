from pydantic import BaseModel
from typing import List, Optional

class MovieShowtime(BaseModel):
    """
    Class to Represent a Showtime with Cinema with required field to show it on 
    billboard catalog
    """
    movie_id: Optional[int]
    title: str
    sinopsis: str
    poster_url: str
    rating: str
    minute_duration: int
    showtimes: List['ShowtimeDetail']
 
class ShowtimeDetail(BaseModel):
    showtime_id: Optional[int]
    type: str # IMAX
    start_time: str
    language: str
    screen: str # Theater ID with Theather {id} 
    total_seats: int
    available_seats: int


class MovieShowtimesFilters(BaseModel):
    cinema_id_list: Optional[List[int]] = [] 
    movie_id: Optional[int]
    incoming: Optional[bool] = True
