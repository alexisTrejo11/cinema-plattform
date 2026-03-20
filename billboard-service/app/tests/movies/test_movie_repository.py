from typing import Any, List
import pytest
from tests.movies.conftest import *

class TestSQLAlchemyMovieRepository:
    
    @pytest.mark.asyncio
    async def test_save_new_movie(self, session: Any, sample_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        
        # Act
        saved_movie = await repository.save(sample_movie)
        await session.commit()
        
        # Assert
        assert saved_movie.id is not None
        assert saved_movie.title == sample_movie.title
        assert saved_movie.original_title == sample_movie.original_title
        assert saved_movie.minute_duration == sample_movie.minute_duration
        assert saved_movie.is_active is True
        assert saved_movie.created_at is not None


    @pytest.mark.asyncio
    async def test_get_by_id_existing_movie(self, session: Any, sample_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        saved_movie = await repository.save(sample_movie)
        await session.commit()
        
        # Act
        assert saved_movie.id is not None
        found_movie = await repository.get_by_id(saved_movie.id)
        
        # Assert
        assert found_movie is not None
        assert found_movie.id == saved_movie.id
        assert found_movie.title == sample_movie.title
    
    @pytest.mark.asyncio
    async def test_get_by_id_non_existing_movie(self, session: Any):
        # Arrange 
        repository = MovieRepository(session)
        
        # Act
        found_movie = await repository.get_by_id(9999)
        
        # Assert
        assert found_movie is None

    @pytest.mark.asyncio
    async def test_get_active_movies(self, session: Any, sample_movie: Movie, inactive_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        await repository.save(sample_movie)
        await repository.save(inactive_movie)
        
        # Act
        active_movies = await repository.list_active()
        
        # Assert
        assert len(active_movies) == 1
        assert active_movies[0].title == sample_movie.title
        assert active_movies[0].is_active == True

    @pytest.mark.asyncio
    async def test_get_all_with_pagination(self, session: Any):
        # Arrange 
        repository = MovieRepository(session)
        
        movies: List[Movie] = []
        for i in range(5):
            movie = Movie(
                title=f"Test Movie {i}",
                original_title=f"Test Movie Original {i}", 
                minute_duration=120,
                release_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31),
                description=f"Test movie {i}",
                genre=MovieGenre.ACTION,
                rating=MovieRating.PG_13,
                is_active=True
            )
            movies.append(await repository.save(movie))
        
        # Act 
        page_params = {'offset': 1, 'limit': 2}
        paginated_movies = await repository.list_all(page_params)
        
        # Assert
        assert len(paginated_movies) == 2

    @pytest.mark.asyncio
    async def test_get_all_default_pagination(self, session: Any, sample_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        await repository.save(sample_movie)
        
        # Act
        movies = await repository.list_all({})
        
        # Assert
        assert len(movies) == 1
        assert movies[0].title == sample_movie.title

    @pytest.mark.asyncio
    async def test_update_existing_movie(self, session: Any, sample_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        saved_movie = await repository.save(sample_movie)
        saved_movie.title = "Updated Title" # Update fields
        saved_movie.description = "Updated description"
        
        # Act
        updated_movie = await repository.save(saved_movie)
        
        # Assert
        assert updated_movie.id == saved_movie.id
        assert updated_movie.title == "Updated Title"
        assert updated_movie.description == "Updated description"

    @pytest.mark.asyncio
    async def test_delete_movie(self, session: Any, sample_movie: Movie):
        # Arrange
        repository = MovieRepository(session)
        saved_movie = await repository.save(sample_movie)
        movie_id = saved_movie.id
        
        # Act
        assert movie_id is not None
        await repository.delete(movie_id)
        
        # Assert
        deleted_movie = await repository.get_by_id(movie_id)
        assert deleted_movie is None

    @pytest.mark.asyncio
    async def test_get_active_movies_empty_result(self, session: Any):
        # Act
        repository = MovieRepository(session)
        active_movies = await repository.list_active()
        
        # Assert
        assert len(active_movies) == 0

    @pytest.mark.asyncio
    async def test_save_movie_without_optional_fields(self, session: Any):
        repository = MovieRepository(session)
        # Arrange
        minimal_movie = Movie(
            title="Minimal Movie",
            minute_duration=90,
            release_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            description="A minimal movie",
            genre=MovieGenre.COMEDY,
            rating=MovieRating.G,
        )
        
        # Act
        saved_movie = await repository.save(minimal_movie)
        
        # Assert
        assert saved_movie.id is not None
        assert saved_movie.title == "Minimal Movie"
        assert saved_movie.original_title is None
        assert saved_movie.poster_url is None
        assert saved_movie.trailer_url is None

