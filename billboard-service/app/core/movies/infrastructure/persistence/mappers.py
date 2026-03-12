from datetime import datetime
from app.core.movies.domain.entities import Movie
from .models import MovieModel


class MovieMapper:
    @staticmethod
    def to_entity(model: MovieModel) -> Movie:
        return Movie(
            id=model.id,
            title=model.title,
            original_title=model.original_title,
            minute_duration=model.minute_duration,
            release_date=model.release_date,
            end_date=model.end_date,
            description=model.description,
            genre=model.genre,
            rating=model.rating,
            poster_url=model.poster_url,
            trailer_url=model.trailer_url,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Movie) -> MovieModel:
        return MovieModel(
            id=entity.id,
            title=entity.title,
            original_title=entity.original_title,
            minute_duration=entity.minute_duration,
            release_date=entity.release_date,
            end_date=entity.end_date,
            description=entity.description,
            genre=entity.genre,
            rating=entity.rating,
            poster_url=str(entity.poster_url) if entity.poster_url else None,
            trailer_url=str(entity.trailer_url) if entity.trailer_url else None,
            is_active=entity.is_active,
            created_at=entity.created_at or datetime.now(),
            updated_at=entity.updated_at or datetime.now(),
        )
