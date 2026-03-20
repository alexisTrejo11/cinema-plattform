from tests.cinema.conftest import *

# -----------------------------
# Test: Create & Read (get_by_id)
# -----------------------------
@pytest.mark.asyncio
async def test_create_and_get_cinema(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    # Arrange
    saved = await cinema_repo.save(sample_cinema)

    # Act
    assert saved.id
    fetched = await cinema_repo.get_by_id(saved.id)

    # Assert
    assert fetched is not None
    assert fetched.name == sample_cinema.name
    assert fetched.tax_number == sample_cinema.tax_number

# -----------------------------
# Test: Update
# -----------------------------
@pytest.mark.asyncio
async def test_update_cinema(cinema_repo: CinemaRepository, sample_cinema: Cinema, updated_cinema_data: Dict[str, Any]):
    saved = await cinema_repo.save(sample_cinema)
    # Apply updates
    for key, value in updated_cinema_data.items():
        setattr(saved, key, value)

    updated = await cinema_repo.save(saved)

    assert updated.name == updated_cinema_data["name"]
    assert updated.description == updated_cinema_data["description"]
    assert updated.is_active == updated_cinema_data["is_active"]
    assert updated.tax_number == updated_cinema_data["tax_number"]


# -----------------------------
# Test: Delete
# -----------------------------
@pytest.mark.asyncio
async def test_delete_cinema(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    saved = await cinema_repo.save(sample_cinema)

    assert saved.id
    await cinema_repo.delete(saved.id)

    assert saved.id
    result = await cinema_repo.get_by_id(saved.id)
    assert result is None


# -----------------------------
# Test: List All Cinemas
# -----------------------------
@pytest.mark.asyncio
async def test_list_all_cinemas(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    await cinema_repo.save(sample_cinema)
    page_params = {"offset": 0, "limit": 10}

    results = await cinema_repo.list_all(page_params)

    assert len(results) >= 1
    assert any(c.name == sample_cinema.name for c in results)


# -----------------------------
# Test: Search Cinemas
# -----------------------------
@pytest.mark.asyncio
async def test_search_cinemas_by_name(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    await cinema_repo.save(sample_cinema)
    page_params = {"offset": 0, "limit": 10}
    filter_params = {"name": "Sample"}

    results = await cinema_repo.search(page_params, filter_params)

    assert len(results) == 1
    assert results[0].name == sample_cinema.name


@pytest.mark.asyncio
async def test_search_cinemas_by_region(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    await cinema_repo.save(sample_cinema)
    page_params = {"offset": 0, "limit": 10}
    filter_params = {"region": sample_cinema.region}

    results = await cinema_repo.search(page_params, filter_params)

    assert len(results) == 1
    assert results[0].region == sample_cinema.region


@pytest.mark.asyncio
async def test_search_cinemas_by_is_active(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    await cinema_repo.save(sample_cinema)
    page_params = {"offset": 0, "limit": 10}
    filter_params = {"is_active": True}

    results = await cinema_repo.search(page_params, filter_params)

    assert len(results) >= 1
    assert all(c.is_active for c in results)


# -----------------------------
# Test: Get Cinemas by Tax Number
# -----------------------------
@pytest.mark.asyncio
async def test_get_cinema_by_tax_number(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    saved = await cinema_repo.save(sample_cinema)

    cinema = await cinema_repo.get_by_tax_number(saved.tax_number)

    assert cinema is not None
    assert cinema.tax_number == saved.tax_number


# -----------------------------
# Test: Filter by Min/Max Screens
# -----------------------------
@pytest.mark.asyncio
async def test_search_by_min_screens(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    sample_cinema.screens = 5
    await cinema_repo.save(sample_cinema)

    filter_params = {"min_screens": 3}
    results = await cinema_repo.search({}, filter_params)

    assert len(results) == 1
    assert results[0].screens >= 3


@pytest.mark.asyncio
async def test_search_by_max_screens(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    sample_cinema.screens = 5
    await cinema_repo.save(sample_cinema)

    filter_params = {"max_screens": 10}
    results = await cinema_repo.search({}, filter_params)

    assert len(results) == 1
    assert results[0].screens <= 10


# -----------------------------
# Test: Filter by Renovation Date
# -----------------------------
@pytest.mark.asyncio
async def test_search_by_renovated_after(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    sample_cinema.last_renovation = date(2020, 1, 1)
    await cinema_repo.save(sample_cinema)

    filter_params = {"renovated_after": date(2019, 1, 1)}
    results = await cinema_repo.search({}, filter_params)

    assert len(results) == 1
    assert results[0].last_renovation
    assert results[0].last_renovation > date(2019, 1, 1)



# -----------------------------
# Test: Get Active Cinemas
# -----------------------------
@pytest.mark.asyncio
async def test_get_active_cinemas(cinema_repo: CinemaRepository, sample_cinema: Cinema):
    inactive_cinema = sample_cinema.model_copy()
    inactive_cinema.is_active = False
    inactive_cinema.contact_info = ContactInfo(phone="+1234567890",email_contact="test-email2@email.com", address="123",location=Location(lat=19.4326, lng=-99.1332))    
    inactive_cinema.name = "Inactive Cinema"
    inactive_cinema.tax_number = "0987654321"

    # Save both
    await cinema_repo.save(sample_cinema)
    await cinema_repo.save(inactive_cinema)
    
    active_cinemas = await cinema_repo.list_active()

    assert len(active_cinemas) == 1
    assert active_cinemas[0].is_active is True