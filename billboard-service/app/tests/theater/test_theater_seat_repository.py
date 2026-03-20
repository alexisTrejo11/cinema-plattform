from tests.theater.conftest import *

# -----------------------------
# Test: Create & Get by ID
# -----------------------------
@pytest.mark.asyncio
async def test_create_and_get_seat(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat):
    # Arange
    saved = await seat_repo.save(sample_seat)

    # Act
    assert saved.id
    fetched = await seat_repo.get_by_id(saved.id)

    # Assert
    assert fetched is not None
    assert fetched.seat_row == sample_seat.seat_row
    assert fetched.seat_number == sample_seat.seat_number
    assert fetched.seat_type == sample_seat.seat_type
    assert fetched.theater_id == sample_seat.theater_id

# -----------------------------
# Test: Update
# -----------------------------
@pytest.mark.asyncio
async def test_update_seat(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat, updated_seat_data: Dict[str, Any]):
    # Arange
    saved = await seat_repo.save(sample_seat)

    # Act
    for key, value in updated_seat_data.items():
        setattr(saved, key, value)
    updated = await seat_repo.save(saved)

    # Assert
    assert updated.seat_row == updated_seat_data["seat_row"]
    assert updated.seat_number == updated_seat_data["seat_number"]
    assert updated.seat_type == updated_seat_data["seat_type"]
    assert updated.is_active == updated_seat_data["is_active"]


# -----------------------------
# Test: Delete
# -----------------------------
@pytest.mark.asyncio
async def test_delete_seat(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat):
    # Arange
    saved = await seat_repo.save(sample_seat)

    # Act
    assert saved.id
    await seat_repo.delete(saved.id)

    # Assert
    result = await seat_repo.get_by_id(saved.id)
    assert result is None


# -----------------------------
# Test: Get by Theater ID
# -----------------------------
@pytest.mark.asyncio
async def test_get_by_theater(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat):
    other_theater_id = 999
    other_seat = sample_seat.model_copy()
    other_seat.theater_id = other_theater_id
    other_seat.seat_number = 2

    await seat_repo.save(sample_seat)
    await seat_repo.save(other_seat)

    results = await seat_repo.get_by_theater(sample_seat.theater_id)

    assert len(results) == 1
    assert results[0].theater_id == sample_seat.theater_id
    assert results[0].seat_row == sample_seat.seat_row
    assert results[0].seat_number == sample_seat.seat_number


# -----------------------------
# Test: Exists by Theater
# -----------------------------
@pytest.mark.asyncio
async def test_exists_by_theater(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat):
    other_theater_id = 999

    await seat_repo.save(sample_seat)

    exists = await seat_repo.exists_by_theater(sample_seat.theater_id)
    assert exists is True

    other_exists = await seat_repo.exists_by_theater(other_theater_id)
    assert other_exists is False


# -----------------------------
# Test: Exists by Seat Values
# -----------------------------
@pytest.mark.asyncio
async def test_exist_by_theater_and_seat_values(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat):
    other_row = "X"
    other_number = 999

    await seat_repo.save(sample_seat)

    exists = await seat_repo.exist_by_theater_and_seat_values(
        sample_seat.theater_id,
        sample_seat.seat_row,
        sample_seat.seat_number
    )
    assert exists is True

    other_exists = await seat_repo.exist_by_theater_and_seat_values(
        sample_seat.theater_id,
        other_row,
        other_number
    )
    assert other_exists is False


# -----------------------------
# Test: Save Fails Gracefully
# -----------------------------
@pytest.mark.asyncio
async def test_save_fails_gracefully(seat_repo: TheaterSeatRepository, sample_seat: TheaterSeat, monkeypatch: "pytest.MonkeyPatch"):
    async def mock_flush(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(seat_repo.session, "flush", mock_flush)

    with pytest.raises(RuntimeError, match="Failed to save seat"):
        await seat_repo.save(sample_seat)


# -----------------------------
# Test: Get Nonexistent Seat
# -----------------------------
@pytest.mark.asyncio
async def test_get_nonexistent_seat(seat_repo: TheaterSeatRepository):
    result = await seat_repo.get_by_id(99999)
    assert result is None