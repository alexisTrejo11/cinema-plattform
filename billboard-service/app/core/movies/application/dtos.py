from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, TYPE_CHECKING
from datetime import date
from app.core.movies.domain.enums import MovieGenre, MovieRating
from app.core.shared.pagination import PaginationResponse

if TYPE_CHECKING:
    from app.core.shared.pagination import Page
    from app.core.movies.domain.entities import Movie


class SearchMovieFilters(BaseModel):
    """Filter parameters for movie search endpoints."""

    title: Optional[str] = Field(
        None,
        description="Filter by (partial) movie title match.",
        examples=["Inception"],
    )
    genre: Optional[MovieGenre] = Field(
        None, description="Filter by movie genre.", examples=[MovieGenre.ACTION]
    )
    rating: Optional[MovieRating] = Field(
        None, description="Filter by movie rating.", examples=[MovieRating.PG_13]
    )
    is_active: Optional[bool] = Field(
        None, description="Filter by active/inactive status.", examples=[True]
    )
    release_date_from: Optional[date] = Field(
        None,
        description="Include movies released on/after this date.",
        examples=["2024-01-01"],
    )
    release_date_to: Optional[date] = Field(
        None,
        description="Include movies released on/before this date.",
        examples=["2024-12-31"],
    )
    min_duration: Optional[int] = Field(
        None, ge=0, description="Minimum movie duration in minutes.", examples=[90]
    )
    max_duration: Optional[int] = Field(
        None, ge=0, description="Maximum movie duration in minutes.", examples=[150]
    )


class MovieSummaryResponse(BaseModel):
    """Lightweight movie response for list/search endpoints."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.isoformat()},
    )

    id: int = Field(..., description="Unique identifier of the movie.", examples=[1])
    title: str = Field(
        ..., description="Movie title.", max_length=200, examples=["Inception"]
    )
    original_title: Optional[str] = Field(
        None, description="Original/original-language title.", examples=["Inception"]
    )
    minute_duration: int = Field(
        ...,
        ge=1,
        description="Duration in minutes.",
        examples=[148],
    )
    release_date: date = Field(
        ..., description="Release date.", examples=["2010-07-16"]
    )
    genre: MovieGenre = Field(
        ..., description="Movie genre.", examples=[MovieGenre.SCI_FI]
    )
    rating: MovieRating = Field(
        ..., description="Movie rating.", examples=[MovieRating.PG_13]
    )
    poster_url: Optional[str] = Field(
        None,
        description="Poster URL.",
        examples=["https://cdn.example.com/posters/1.jpg"],
    )
    is_active: bool = Field(
        ...,
        description="Whether the movie is currently active.",
        examples=[True],
    )


class MovieDetailResponse(BaseModel):
    """Detailed movie response for get-by-id endpoints."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.isoformat()},
    )

    id: int = Field(..., description="Unique identifier of the movie.", examples=[1])
    title: str = Field(
        ..., description="Movie title.", max_length=200, examples=["Inception"]
    )
    original_title: Optional[str] = Field(
        None,
        description="Original/original-language title.",
        examples=["Inception"],
    )
    minute_duration: int = Field(
        ...,
        ge=1,
        description="Duration in minutes.",
        examples=[148],
    )
    release_date: date = Field(
        ..., description="Release date.", examples=["2010-07-16"]
    )
    end_date: date = Field(
        ..., description="End date for current programming.", examples=["2010-12-31"]
    )
    description: str = Field(
        ..., description="Movie synopsis/description.", examples=["A thief who steals..."]
    )
    genre: MovieGenre = Field(
        ..., description="Movie genre.", examples=[MovieGenre.SCI_FI]
    )
    rating: MovieRating = Field(
        ..., description="Movie rating.", examples=[MovieRating.PG_13]
    )
    poster_url: Optional[str] = Field(
        None,
        description="Poster URL.",
        examples=["https://cdn.example.com/posters/1.jpg"],
    )
    trailer_url: Optional[str] = Field(
        None,
        description="Trailer URL.",
        examples=["https://youtube.com/watch?v=example"],
    )
    is_active: bool = Field(..., description="Whether the movie is active.", examples=[True])


class PaginatedMovieResponse(PaginationResponse):
    """Paginated response for movie list/search endpoints."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "data": [
                        {
                            "id": 1,
                            "title": "Inception",
                            "original_title": "Inception",
                            "minute_duration": 148,
                            "release_date": "2010-07-16",
                            "genre": "SCI_FI",
                            "rating": "PG_13",
                            "poster_url": "https://cdn.example.com/posters/1.jpg",
                            "is_active": True,
                        }
                    ],
                    "page_size": 10,
                    "total_items": 42,
                    "total_pages": 5,
                    "current_page": 1,
                    "next_page": 2,
                    "previous_page": 1,
                    "has_next": True,
                    "has_previous": False,
                }
            ]
        }
    )

    data: List[MovieSummaryResponse]

    @classmethod
    def from_page(cls, page: "Page[Movie]") -> "PaginatedMovieResponse":
        """
        Convert a Page[Movie] domain object to PaginatedMovieResponse DTO.

        Args:
            page: Page object containing Movie entities and pagination metadata

        Returns:
            PaginatedMovieResponse with converted data
        """
        movie_summaries = [
            MovieSummaryResponse.model_validate(movie.model_dump(mode="json"))
            for movie in page.items
        ]

        return cls(
            data=movie_summaries,
            page_size=page.page_size,
            total_items=page.total,
            total_pages=page.total_pages,
            current_page=page.page,
            next_page=(
                min(page.page + 1, page.total_pages) if page.has_next else page.page
            ),
            previous_page=max(page.page - 1, 1) if page.has_previous else page.page,
            has_next=page.has_next,
            has_previous=page.has_previous,
        )


class MovieShowtime(BaseModel):
    """
    Class to Represent a Showtime with Cinema with required field to show it on
    billboard catalog
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "movie_id": 1,
                    "title": "Inception",
                    "sinopsis": "A thief who steals...",
                    "poster_url": "https://cdn.example.com/posters/1.jpg",
                    "rating": "PG_13",
                    "minute_duration": 148,
                    "showtimes": [
                        {
                            "showtime_id": 10,
                            "type": "IMAX",
                            "start_time": "2026-03-19T20:30:00Z",
                            "language": "EN",
                            "screen": "Room - 3",
                            "total_seats": 200,
                            "available_seats": 48,
                        }
                    ],
                }
            ]
        },
    )

    movie_id: Optional[int] = Field(
        None, description="Movie identifier.", examples=[1]
    )
    title: str = Field(..., description="Movie title.", examples=["Inception"])
    sinopsis: str = Field(
        ..., description="Movie synopsis.", examples=["A thief who steals..."]
    )
    poster_url: str = Field(
        ..., description="Poster URL.", examples=["https://cdn.example.com/posters/1.jpg"]
    )
    rating: str = Field(
        ..., description="Rating label (e.g. G/PG/PG_13).", examples=["PG_13"]
    )
    minute_duration: int = Field(
        ..., ge=1, description="Duration in minutes.", examples=[148]
    )
    showtimes: List["ShowtimeDetail"] = Field(
        ..., description="Showtimes for the movie."
    )


class ShowtimeDetail(BaseModel):
    showtime_id: Optional[int] = Field(
        None, description="Showtime identifier.", examples=[10]
    )
    type: str = Field(..., description="Screening type (e.g. IMAX, 3D).", examples=["IMAX"])
    start_time: str = Field(
        ..., description="Show start time (ISO-8601).", examples=["2026-03-19T20:30:00Z"]
    )
    language: str = Field(..., description="Language code/name.", examples=["EN"])
    screen: str = Field(
        ..., description="Screen/room label.", examples=["Room - 3"]
    )
    total_seats: int = Field(..., ge=0, description="Total seats for the show.", examples=[200])
    available_seats: int = Field(
        ..., ge=0, description="Available seats for the show.", examples=[48]
    )


class MovieShowtimesFilters(BaseModel):
    """Filters for retrieving movie showtimes grouped by movie."""

    cinema_id_list: Optional[List[int]] = Field(
        default=None,
        description="Optional list of cinema IDs to filter by.",
        examples=[[1, 2]],
    )
    movie_id: Optional[int] = Field(
        None, description="Optional movie ID to filter by.", examples=[3]
    )
    incoming: Optional[bool] = Field(
        True,
        description="If true, include only upcoming showtimes; if false, include released/past data (depending on repository logic).",
        examples=[False],
    )


class MovieShowtimeResponse(MovieShowtime):
    """
    Response model for `GET /movies/showtimes/schedule-details`.

    Alias of `MovieShowtime` kept to maintain compatibility with the existing controller.
    """

    pass
