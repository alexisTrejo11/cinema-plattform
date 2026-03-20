from tests.theater.conftest import *

# -----------------------------
# Test: Create & Get by ID
# -----------------------------
@pytest.mark.asyncio
async def test_create_and_get_theater(theater_repo: TheaterRepository, sample_theater: Theater):
    # Arrange
    saved = await theater_repo.save(sample_theater)

    # Act
    assert saved.id
    fetched = await theater_repo.get_by_id(saved.id)

    # Assert    
    assert fetched is not None
    assert fetched.name == sample_theater.name
    assert fetched.capacity == sample_theater.capacity
    assert fetched.theater_type == sample_theater.theater_type
    assert fetched.cinema_id == sample_theater.cinema_id


# -----------------------------
# Test: Update
# -----------------------------
@pytest.mark.asyncio
async def test_update_theater(theater_repo: TheaterRepository, sample_theater: Theater, updated_theater_data: Dict[str, Any]):
    # Arrange
    saved = await theater_repo.save(sample_theater)
    for key, value in updated_theater_data.items():
        setattr(saved, key, value)

    # Act
    updated = await theater_repo.save(saved)

    # Assert
    assert updated.name == updated_theater_data["name"]
    assert updated.capacity == updated_theater_data["capacity"]
    assert updated.theater_type == updated_theater_data["theater_type"]
    assert updated.is_active == updated_theater_data["is_active"]
    assert updated.maintenance_mode == updated_theater_data["maintenance_mode"]

# -----------------------------
# Test: Delete
# -----------------------------
@pytest.mark.asyncio
async def test_delete_theater(theater_repo: TheaterRepository, sample_theater: Theater):
    saved = await theater_repo.save(sample_theater)

    assert saved.id
    await theater_repo.delete(saved.id)

    result = await theater_repo.get_by_id(saved.id)
    assert result is None


# -----------------------------
# Test: List All Theaters
# -----------------------------
@pytest.mark.asyncio
async def test_list_all_theaters(theater_repo: TheaterRepository, sample_theater: Theater):
    await theater_repo.save(sample_theater)
    page_params = {"offset": 0, "limit": 10}

    results = await theater_repo.list_all(page_params)

    assert len(results) >= 1
    assert any(t.name == sample_theater.name for t in results)

# -----------------------------
# Test: List Theaters by Cinema ID
# -----------------------------
@pytest.mark.asyncio
async def test_list_by_cinema(theater_repo: TheaterRepository, sample_theater: Theater):
    other_cinema_id = 999
    sample_theater_other_cinema = sample_theater.copy()
    sample_theater_other_cinema.cinema_id = other_cinema_id
    sample_theater_other_cinema.name = "Other Theater"

    await theater_repo.save(sample_theater)
    await theater_repo.save(sample_theater_other_cinema)

    results = await theater_repo.list_by_cinema(sample_theater.cinema_id)

    assert len(results) == 1
    assert results[0].cinema_id == sample_theater.cinema_id
    assert results[0].name == sample_theater.name

    other_results = await theater_repo.list_by_cinema(other_cinema_id)
    assert len(other_results) == 1
    assert other_results[0].cinema_id == other_cinema_id


# -----------------------------
# Test: Save Fails Gracefully
# -----------------------------
@pytest.mark.asyncio
async def test_save_fails_gracefully(theater_repo: TheaterRepository, sample_theater: Theater, monkeypatch: "pytest.MonkeyPatch"):
    async def mock_flush(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(theater_repo.session, "flush", mock_flush)

    with pytest.raises(RuntimeError, match="Failed to save theater"):
        await theater_repo.save(sample_theater)


# -----------------------------
# Test: Get Nonexistent Theater
# -----------------------------
@pytest.mark.asyncio
async def test_get_nonexistent_theater(theater_repo: TheaterRepository):
    result = await theater_repo.get_by_id(99999)
    assert result is None