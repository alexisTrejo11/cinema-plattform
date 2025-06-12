from typing import List, Dict
from app.movies.domain.entities import Movie
from app.showtime.domain.entities.showtime import Showtime
from .dtos import MovieShowtime, ShowtimeDetail

class MovieShowtimeService:
    @classmethod
    def generate_movie_showtimes(cls, movies: List[Movie], showtimes_by_movie: Dict[int, List[Showtime]]
    ) -> List[MovieShowtime]:        
        return [
            cls._create_movie_showtime(movie, showtimes_by_movie.get(movie.id, []))
            for movie in movies
        ]

    @classmethod
    def _create_movie_showtime(
        cls, 
        movie: Movie, 
        showtimes: List[Showtime]
    ) -> MovieShowtime:
        return MovieShowtime(
            movie_id= movie.id,
            title=movie.title,
            poster_url=str(movie.poster_url),
            minute_duration=movie.minute_duration,
            sinopsis=movie.description,
            rating=movie.rating,
            showtimes=cls._create_showtimes_details(showtimes),
        )

    @classmethod
    def _create_showtimes_details(cls, showtimes: List[Showtime]) -> List[ShowtimeDetail]:
        showtimes_dtos = []
        
        for showtime in showtimes:
            dto = ShowtimeDetail(
                showtime_id=showtime.id,
                type=showtime.type,
                start_time=str(showtime.start_time),
                language=showtime.language,
                screen=f"Room - {showtime.theater_id}",
                total_seats=showtime.total_seats if showtime.total_seats is not None else 0,
                avaailable_seats=showtime.avaialble_seats,
            )
            showtimes_dtos.append(dto)

        return showtimes_dtos
