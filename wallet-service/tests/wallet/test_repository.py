from decimal import Decimal
import pytest
import pytest_asyncio
from datetime import datetime, timezone
import uuid

from app.user.domain.user import User, UserId, UserRole
from app.user.infrastructure.sql_user_respository import (
    SqlAlchemyUserRepository,
)

from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.value_objects import (
    Money,
    Currency,
    WalletId,
)
from app.wallet.infrastructure.persistence.sql.sqlalchemy_models import WalletSQLModel
from app.wallet.infrastructure.persistence.sql.wallet_repository import (
    SqlAlchemyWalletRepository as WalletRepository,
    WalletNotFoundError,
)


@pytest_asyncio.fixture(scope="function")
async def user_repo(session) -> SqlAlchemyUserRepository:
    """Provides an instance of the SqlAlchemyUserRepository for testing."""
    return SqlAlchemyUserRepository(session)


@pytest_asyncio.fixture
async def existing_user_for_wallet_test(
    user_repo: SqlAlchemyUserRepository,
    request,
) -> User:
    user_id_to_use = getattr(request, "param", UserId(uuid.uuid4()))

    user_data = {
        "id": user_id_to_use,
        "email": f"wallet_test_user_{uuid.uuid4().hex[:8]}@example.com",
        "roles": [UserRole.CUSTOMER],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }

    created_user = await user_repo.save(user_data)
    await user_repo.session.commit()

    yield created_user


@pytest_asyncio.fixture(scope="function")
async def wallet_repo(session) -> WalletRepository:
    """Provides an instance of the SqlAlchemyWalletRepository for testing."""
    return WalletRepository(session)


@pytest.fixture
def sample_wallet_entity_data():
    """Provides base data for a wallet creation, but without a concrete UserId yet."""
    return {"initial_currency": Currency.USD}


@pytest.fixture
def wallet_entity_for_test(
    existing_user_for_wallet_test: User,
    sample_wallet_entity_data: dict,
) -> Wallet:
    """
    Provides a Wallet domain entity created with the UserId of an existing,
    persisted user.
    """
    user_id_for_wallet = existing_user_for_wallet_test.get_id()

    return Wallet.create(
        user_id=user_id_for_wallet,
        initial_currency=sample_wallet_entity_data["initial_currency"],
    )


@pytest.mark.asyncio
async def test_create_wallet_successfully(
    wallet_repo: WalletRepository,
    wallet_entity_for_test: Wallet,
):
    """
    Tests that a wallet can be successfully created and saved for an existing user.
    """
    created_wallet = await wallet_repo.create(wallet_entity_for_test)

    assert isinstance(created_wallet.id, WalletId)
    assert created_wallet.id is not None
    assert isinstance(created_wallet.user_id, UserId)
    assert created_wallet.user_id.value == wallet_entity_for_test.user_id.value
    assert isinstance(created_wallet.balance, Money)
    assert created_wallet.balance.amount == Decimal("0.00")
    assert created_wallet.balance.currency == Currency.USD

    db_wallet = await wallet_repo.session.get(WalletSQLModel, created_wallet.id.value)
    assert db_wallet is not None
    assert db_wallet.user_id == created_wallet.user_id.value
    assert db_wallet.balance_amount == created_wallet.balance.amount
    assert db_wallet.balance_currency.value == created_wallet.balance.currency.value


@pytest.mark.asyncio
async def test_get_by_id_found(
    wallet_repo: WalletRepository,
    wallet_entity_for_test: Wallet,
):
    """Tests retrieving a wallet by its ID when it exists."""
    # Arrange: Create and save a wallet
    saved_wallet = await wallet_repo.create(wallet_entity_for_test)

    # Act
    retrieved_wallet = await wallet_repo.get_by_id(saved_wallet.id)

    # Assert
    assert retrieved_wallet is not None
    assert retrieved_wallet.id.value == saved_wallet.id.value
    assert retrieved_wallet.user_id.value == saved_wallet.user_id.value
    assert retrieved_wallet.balance == saved_wallet.balance


@pytest.mark.asyncio
async def test_get_by_id_not_found(
    wallet_repo: WalletRepository,
):
    """Tests retrieving a wallet by its ID when it does not exist."""
    # Act
    non_existent_id = WalletId(uuid.uuid4())
    retrieved_wallet = await wallet_repo.get_by_id(non_existent_id)

    # Assert
    assert retrieved_wallet is None


@pytest.mark.asyncio
async def test_get_by_id_not_found_raises_exception(
    wallet_repo: WalletRepository,
):
    """Tests that get_by_id raises WalletNotFoundError when not found and raise_exception is True."""
    # Act & Assert
    non_existent_id = WalletId(uuid.uuid4())
    with pytest.raises(WalletNotFoundError) as exc_info:
        await wallet_repo.get_by_id(non_existent_id, raise_exception=True)

    assert str(non_existent_id.value) in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_by_user_id_found(
    wallet_repo: WalletRepository,
    wallet_entity_for_test: Wallet,
):
    """Tests retrieving a wallet by its user ID when it exists."""
    # Arrange: Create and save a wallet
    saved_wallet = await wallet_repo.create(wallet_entity_for_test)

    # Act
    retrieved_wallet = await wallet_repo.get_by_user_id(saved_wallet.user_id)

    # Assert
    assert retrieved_wallet is not None
    assert retrieved_wallet.id.value == saved_wallet.id.value
    assert retrieved_wallet.user_id.value == saved_wallet.user_id.value
    assert retrieved_wallet.balance.amount == saved_wallet.balance.amount


@pytest.mark.asyncio
async def test_get_by_user_id_not_found(
    wallet_repo: WalletRepository,
):
    """Tests retrieving a wallet by its user ID when it does not exist."""
    # Act
    non_existent_user_id = UserId(uuid.uuid4())
    retrieved_wallet = await wallet_repo.get_by_user_id(non_existent_user_id)

    # Assert
    assert retrieved_wallet is None


@pytest.mark.asyncio
async def test_get_by_user_id_not_found_raises_exception(
    wallet_repo: WalletRepository,
):
    """Tests that get_by_user_id raises WalletNotFoundError when not found and raise_exception is True."""
    # Act & Assert
    non_existent_user_id = UserId(uuid.uuid4())
    with pytest.raises(WalletNotFoundError) as exc_info:
        await wallet_repo.get_by_user_id(non_existent_user_id, raise_exception=True)

    assert str(non_existent_user_id.value) in str(exc_info.value)
