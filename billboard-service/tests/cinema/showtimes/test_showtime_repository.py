from typing import Optional
from app.shared.pagination import PaginationParams
from app.movies.application.dtos import MovieShowtimesFilters
from app.showtime.domain.enums import ShowtimeType
from tests.showtimes.constest import *


@pytest.mark.asyncio
async def test_save_and_get_by_id(
    showtime_repo: ShowtimeRepository, sample_showtime: Showtime
):
    # Arrange
    # sample_showtime se crea con id=None, lo que indica una nueva entidad

    # Act
    saved_showtime = await showtime_repo.save(sample_showtime)
    assert saved_showtime.id
    fetched_showtime = await showtime_repo.get_by_id(saved_showtime.id)

    # Assert
    assert saved_showtime.id is not None
    assert fetched_showtime is not None
    assert fetched_showtime.id == saved_showtime.id
    assert fetched_showtime.movie_id == sample_showtime.movie_id
    assert fetched_showtime.cinema_id == sample_showtime.cinema_id

    assert (
        abs((fetched_showtime.start_time - sample_showtime.start_time).total_seconds())
        < 1
    )
    assert fetched_showtime.price == sample_showtime.price


@pytest.mark.asyncio
async def test_update_showtime(
    showtime_repo: ShowtimeRepository,
    sample_showtime: Showtime,
    showtime_for_update: Dict[str, Any],
):
    # Arrange
    saved_showtime = await showtime_repo.save(sample_showtime)

    # app. updates
    for key, value in showtime_for_update.items():
        setattr(saved_showtime, key, value)

    # Act
    updated_showtime = await showtime_repo.save(saved_showtime)
    assert updated_showtime.id
    fetched_showtime: Optional[Showtime] = await showtime_repo.get_by_id(
        updated_showtime.id
    )

    # Assert
    assert fetched_showtime
    assert updated_showtime.id == saved_showtime.id
    assert fetched_showtime.price == showtime_for_update["price"]
    assert fetched_showtime.type == showtime_for_update["type"]
    assert fetched_showtime.language == showtime_for_update["language"]


@pytest.mark.asyncio
async def test_delete_showtime(
    showtime_repo: ShowtimeRepository, sample_showtime: Showtime
):
    # Arrange
    saved_showtime = await showtime_repo.save(sample_showtime)
    assert saved_showtime.id

    assert await showtime_repo.get_by_id(saved_showtime.id) is not None

    # Act
    await showtime_repo.delete(saved_showtime.id)

    # Assert
    result = await showtime_repo.get_by_id(saved_showtime.id)
    assert result is None


@pytest.mark.asyncio
async def test_list_all_showtimes(
    showtime_repo: ShowtimeRepository, sample_showtime: Showtime, old_showtime: Showtime
):
    # Arrange
    saved_sample_showtime = await showtime_repo.save(sample_showtime)
    saved_old_showtime = await showtime_repo.save(old_showtime)
    page_params = {"offset": 0, "limit": 10}

    # Act
    results = await showtime_repo.list_all(page_params)

    # Assert
    assert len(results) >= 2
    assert any(s.id == saved_sample_showtime.id for s in results)
    assert any(s.id == saved_old_showtime.id for s in results)


@pytest.mark.asyncio
async def test_list_incoming_by_cinema(
    showtime_repo: ShowtimeRepository,
    sample_showtime: Showtime,
    old_showtime: Showtime,
    future_showtime_different_cinema: Showtime,
):
    # Arrange
    sample_showtime.cinema_id = 1
    sample_showtime.start_time = datetime.now(timezone.utc) + timedelta(hours=1)
    sample_showtime = await showtime_repo.save(sample_showtime)

    old_showtime.cinema_id = 1
    old_showtime.start_time = datetime.now(timezone.utc) - timedelta(hours=1)
    old_showtime = await showtime_repo.save(old_showtime)

    future_showtime_different_cinema.start_time = datetime.now(
        timezone.utc
    ) + timedelta(hours=3)
    future_showtime_different_cinema = await showtime_repo.save(
        future_showtime_different_cinema
    )

    # Act
    incoming_showtimes = await showtime_repo.list_incoming_by_cinema(1)

    # Assert
    assert len(incoming_showtimes) == 1
    assert incoming_showtimes[0].id == sample_showtime.id
    assert incoming_showtimes[0].cinema_id == 1
    assert incoming_showtimes[0].start_time >= datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    assert incoming_showtimes[0].start_time < (
        datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        + timedelta(days=1)
    )


@pytest.mark.asyncio
async def test_list_incoming_by_movie(
    showtime_repo: ShowtimeRepository,
    sample_showtime: Showtime,
    old_showtime: Showtime,
    future_showtime_different_cinema: Showtime,
):
    # Arrange
    sample_showtime.movie_id = 1
    sample_showtime.start_time = datetime.now(timezone.utc) + timedelta(hours=1)
    sample_showtime = await showtime_repo.save(sample_showtime)

    old_showtime.movie_id = 1
    old_showtime.start_time = datetime.now(timezone.utc) - timedelta(hours=1)
    old_showtime = await showtime_repo.save(old_showtime)

    # Other Movie
    future_showtime_different_cinema.movie_id = 99
    future_showtime_different_cinema.start_time = datetime.now(
        timezone.utc
    ) + timedelta(hours=3)
    future_showtime_different_cinema = await showtime_repo.save(
        future_showtime_different_cinema
    )

    # Act
    incoming_showtimes = await showtime_repo.list_incoming_by_movie(1)

    # Assert
    assert len(incoming_showtimes) == 1
    assert incoming_showtimes[0].id == sample_showtime.id
    assert incoming_showtimes[0].movie_id == 1
    assert incoming_showtimes[0].start_time >= datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    assert incoming_showtimes[0].start_time < (
        datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        + timedelta(days=1)
    )


@pytest.mark.asyncio
async def test_list_by_theater_and_date_range(showtime_repo: ShowtimeRepository):
    # Arrange
    theater_id = 10

    # Showtime dentro del rango
    showtime1 = Showtime(
        id=None,
        movie_id=1,
        cinema_id=1,
        theater_id=theater_id,
        seats=[],
        start_time=datetime(2025, 6, 15, 10, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc),
        available_seats=50,
        total_seats=50,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    saved_showtime1 = await showtime_repo.save(showtime1)

    # Showtime fuera del rango (antes)
    showtime_before = Showtime(
        id=None,
        movie_id=2,
        cinema_id=1,
        theater_id=theater_id,
        seats=[],
        start_time=datetime(2025, 6, 14, 8, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 6, 14, 9, 0, tzinfo=timezone.utc),
        available_seats=50,
        total_seats=50,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    await showtime_repo.save(showtime_before)

    # Showtime fuera del rango (después)
    showtime_after = Showtime(
        id=None,
        movie_id=3,
        cinema_id=1,
        theater_id=theater_id,
        seats=[],
        start_time=datetime(2025, 6, 16, 14, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 6, 16, 16, 0, tzinfo=timezone.utc),
        available_seats=50,
        total_seats=50,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    await showtime_repo.save(showtime_after)

    # Showtime para otro teatro
    showtime_other_theater = Showtime(
        id=None,
        movie_id=4,
        cinema_id=1,
        theater_id=11,
        seats=[],
        start_time=datetime(2025, 6, 15, 11, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 6, 15, 13, 0, tzinfo=timezone.utc),
        available_seats=50,
        total_seats=50,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    await showtime_repo.save(showtime_other_theater)

    start_check = datetime(2025, 6, 15, 9, 0, tzinfo=timezone.utc)
    end_check = datetime(2025, 6, 15, 13, 0, tzinfo=timezone.utc)

    # Act
    results = await showtime_repo.list_by_theater_and_date_range(
        theater_id=theater_id,
        start_time_to_check=start_check,
        end_time_to_check=end_check,
    )

    # Assert
    assert len(results) == 1
    assert results[0].id == saved_showtime1.id
    assert results[0].theater_id == theater_id

    # Test con exclusión
    showtime_overlap = Showtime(
        id=None,
        movie_id=5,
        cinema_id=1,
        theater_id=theater_id,
        seats=[],
        start_time=datetime(2025, 6, 15, 11, 30, tzinfo=timezone.utc),
        end_time=datetime(2025, 6, 15, 13, 30, tzinfo=timezone.utc),
        available_seats=50,
        total_seats=50,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    saved_showtime_overlap = await showtime_repo.save(showtime_overlap)

    results_with_exclude = await showtime_repo.list_by_theater_and_date_range(
        theater_id=theater_id,
        start_time_to_check=datetime(2025, 6, 15, 10, 0, tzinfo=timezone.utc),
        end_time_to_check=datetime(2025, 6, 15, 14, 0, tzinfo=timezone.utc),
        exclude_showtime_id=saved_showtime_overlap.id,
    )
    assert saved_showtime1 in results_with_exclude
    assert saved_showtime_overlap not in results_with_exclude
    assert len(results_with_exclude) == 1


@pytest.mark.asyncio
async def test_list_by_filters_group_by_movie(showtime_repo: ShowtimeRepository):
    # Arrange
    # Showtime 1: incoming, cinema_id=1, movie_id=10
    showtime_m1_c1_future = Showtime(
        id=None,
        movie_id=10,
        cinema_id=1,
        theater_id=1,
        seats=[],
        start_time=datetime.now(timezone.utc).replace(microsecond=0)
        + timedelta(hours=1),
        end_time=datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3),
        available_seats=10,
        total_seats=10,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    # CAPTURE THE SAVED OBJECT WITH ITS ID
    saved_showtime_m1_c1_future = await showtime_repo.save(showtime_m1_c1_future)

    # Showtime 2: incoming, cinema_id=2, movie_id=10
    showtime_m1_c2_future = Showtime(
        id=None,
        movie_id=10,
        cinema_id=2,
        theater_id=1,
        seats=[],
        start_time=datetime.now(timezone.utc).replace(microsecond=0)
        + timedelta(hours=2),
        end_time=datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=4),
        available_seats=10,
        total_seats=10,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    # CAPTURE THE SAVED OBJECT WITH ITS ID
    saved_showtime_m1_c2_future = await showtime_repo.save(showtime_m1_c2_future)

    # Showtime 3: incoming, cinema_id=1, movie_id=20
    showtime_m2_c1_future = Showtime(
        id=None,
        movie_id=20,
        cinema_id=1,
        theater_id=2,
        seats=[],
        start_time=datetime.now(timezone.utc).replace(microsecond=0)
        + timedelta(hours=3),
        end_time=datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=5),
        available_seats=10,
        total_seats=10,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    # CAPTURE THE SAVED OBJECT WITH ITS ID
    saved_showtime_m2_c1_future = await showtime_repo.save(showtime_m2_c1_future)

    # Showtime 4: NOT incoming (past), cinema_id=1, movie_id=10
    showtime_m1_c1_past = Showtime(
        id=None,
        movie_id=10,
        cinema_id=1,
        theater_id=1,
        seats=[],
        start_time=datetime.now(timezone.utc).replace(microsecond=0)
        - timedelta(days=1),
        end_time=datetime.now(timezone.utc).replace(microsecond=0)
        - timedelta(days=1, hours=2),
        available_seats=10,
        total_seats=10,
        price=Decimal("10.0"),
        type=ShowtimeType.TRADITIONAL_2D,
        language=ShowtimeLanguage.ORIGINAL_ENGLISH,
    )
    # CAPTURE THE SAVED OBJECT WITH ITS ID
    saved_showtime_m1_c1_past = await showtime_repo.save(showtime_m1_c1_past)

    # Define filters and pagination
    page_data = PaginationParams(offset=0, limit=10)

    # --- Test 1: Incoming only ---
    filters_incoming = MovieShowtimesFilters(movie_id=None, incoming=True)
    result_incoming = await showtime_repo.list_by_filters_group_by_movie(
        filters_incoming, page_data
    )

    assert len(result_incoming) == 2  # Movie 10 and Movie 20
    assert 10 in result_incoming
    assert 20 in result_incoming
    assert (
        len(result_incoming[10]) == 2
    )  # saved_showtime_m1_c1_future, saved_showtime_m1_c2_future
    assert len(result_incoming[20]) == 1  # saved_showtime_m2_c1_future

    # Assert specific IDs are present using the saved objects
    assert any(s.id == saved_showtime_m1_c1_future.id for s in result_incoming[10])
    assert any(s.id == saved_showtime_m1_c2_future.id for s in result_incoming[10])
    assert any(s.id == saved_showtime_m2_c1_future.id for s in result_incoming[20])

    # --- Test 2: Incoming and cinema_id_list ---
    filters_incoming_cinema_1 = MovieShowtimesFilters(
        incoming=True, movie_id=None, cinema_id_list=[1]
    )
    result_incoming_cinema_1 = await showtime_repo.list_by_filters_group_by_movie(
        filters_incoming_cinema_1, page_data
    )

    assert len(result_incoming_cinema_1) == 2  # Movie 10 and Movie 20
    assert 10 in result_incoming_cinema_1
    assert 20 in result_incoming_cinema_1
    assert len(result_incoming_cinema_1[10]) == 1  # saved_showtime_m1_c1_future
    assert len(result_incoming_cinema_1[20]) == 1  # saved_showtime_m2_c1_future

    # Assert specific IDs
    assert any(
        s.id == saved_showtime_m1_c1_future.id for s in result_incoming_cinema_1[10]
    )
    assert any(
        s.id == saved_showtime_m2_c1_future.id for s in result_incoming_cinema_1[20]
    )

    # --- Test 3: Incoming and movie_id ---
    filters_incoming_movie_10 = MovieShowtimesFilters(incoming=True, movie_id=10)
    result_incoming_movie_10 = await showtime_repo.list_by_filters_group_by_movie(
        filters_incoming_movie_10, page_data
    )

    assert len(result_incoming_movie_10) == 1  # Only Movie 10
    assert 10 in result_incoming_movie_10
    assert 20 not in result_incoming_movie_10
    assert (
        len(result_incoming_movie_10[10]) == 2
    )  # saved_showtime_m1_c1_future, saved_showtime_m1_c2_future

    # Assert specific IDs
    assert any(
        s.id == saved_showtime_m1_c1_future.id for s in result_incoming_movie_10[10]
    )
    assert any(
        s.id == saved_showtime_m1_c2_future.id for s in result_incoming_movie_10[10]
    )

    # --- Test 4: Combination of all filters ---
    filters_all_combined = MovieShowtimesFilters(
        incoming=True, cinema_id_list=[1], movie_id=10
    )
    result_all_combined = await showtime_repo.list_by_filters_group_by_movie(
        filters_all_combined, page_data
    )

    assert len(result_all_combined) == 1  # Only Movie 10
    assert 10 in result_all_combined
    assert len(result_all_combined[10]) == 1  # saved_showtime_m1_c1_future

    # Assert specific ID
    assert any(s.id == saved_showtime_m1_c1_future.id for s in result_all_combined[10])

    # --- Test 5: No filters (pagination only) ---
    filters_no_filters = MovieShowtimesFilters(
        movie_id=None, incoming=False
    )  # Explicitly setting incoming=False
    result_no_filters = await showtime_repo.list_by_filters_group_by_movie(
        filters_no_filters, page_data
    )

    # Expected: 2 movies (10 and 20). Movie 10 has 3 showtimes (future c1, future c2, past c1). Movie 20 has 1 showtime (future c1).
    assert len(result_no_filters) == 2  # Expecting movies 10 and 20
    assert 10 in result_no_filters
    assert 20 in result_no_filters

    # Ensure all showtimes are present across all movies
    all_retrieved_showtimes = [
        s for movie_showtimes in result_no_filters.values() for s in movie_showtimes
    ]

    assert any(s.id == saved_showtime_m1_c1_future.id for s in all_retrieved_showtimes)
    assert any(s.id == saved_showtime_m1_c2_future.id for s in all_retrieved_showtimes)
    assert any(s.id == saved_showtime_m2_c1_future.id for s in all_retrieved_showtimes)
    assert any(s.id == saved_showtime_m1_c1_past.id for s in all_retrieved_showtimes)

    # Further check counts for each movie group
    assert len(result_no_filters[10]) == 3  # Expecting all 3 showtimes for movie 10
    assert (
        len(result_no_filters[20]) == 1
    )  # Expecting only the future showtime for movie 20
