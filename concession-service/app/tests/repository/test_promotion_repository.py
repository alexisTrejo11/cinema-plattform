import logging
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.products.infrastructure.persistence.repositories.sqlalchemy_product_repo import (
    SqlAlchemyProductRepository,
)
from app.promotions.application.queries import GetPromotionByProductIdQuery
from app.promotions.domain.entities.promotion import Promotion
from app.promotions.infrastructure.persistence.model.promotion_model import (
    PromotionModel,
)
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository as PromotionRepo,
)
from app.shared.base_exceptions import DatabaseException
from app.shared.pagination import PaginationQuery
from tests.repository.fixture.combos_fixtures import *  # noqa: F403


class TestSQLAlchemyPromotionRepository:
    @pytest.mark.asyncio
    async def test_get_by_id_existing_promotion(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange
        # Crear una promoción de prueba
        promotion = Promotion(**sample_promotion_data, id=PromotionId.generate())
        await promotion_repository.create(promotion)

        # Act
        retrieved_promotion = await promotion_repository.get_by_id(promotion.id)

        # Assert
        assert retrieved_promotion is not None
        assert retrieved_promotion.id == promotion.id
        assert retrieved_promotion.name == promotion.name
        assert retrieved_promotion.rule == promotion.rule
        assert retrieved_promotion.is_active == promotion.is_active

    @pytest.mark.asyncio
    async def test_get_by_id_non_existent_promotion(self, promotion_repository):
        # Arrange
        non_existent_id = PromotionId.generate()

        # Act
        result = await promotion_repository.get_by_id(non_existent_id)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_inactive_promotion(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange
        promotion_data = sample_promotion_data.copy()
        promotion_data["is_active"] = False
        promotion = Promotion(**promotion_data, id=PromotionId.generate())
        await promotion_repository.create(promotion)

        # Act
        result = await promotion_repository.get_by_id(promotion.id)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_with_products(
        self, promotion_repository, session, sample_product, sample_promotion_data
    ):
        # Arrange
        # Guardar producto primero
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        # Crear promoción asociada al producto
        promotion_data = sample_promotion_data.copy()
        promotion_data["applicable_product_ids"] = [sample_product.id]
        promotion = Promotion(**promotion_data, id=PromotionId.generate())
        await promotion_repository.create(promotion)

        # Act
        retrieved_promotion = await promotion_repository.get_by_id(promotion.id)

        # Assert
        assert retrieved_promotion is not None
        assert len(retrieved_promotion.applicable_product_ids) == 1
        assert retrieved_promotion.applicable_product_ids[0] == sample_product.id

    @pytest.mark.asyncio
    async def test_get_by_id_database_error(self, promotion_repository, mocker):
        # Arrange
        mock_session = mocker.AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("Database error")
        repo = PromotionRepo(mock_session)
        test_id = PromotionId.generate()

        # Act & Assert
        with pytest.raises(DatabaseException):
            await repo.get_by_id(test_id)

    @pytest.mark.asyncio
    async def test_get_active_promotions_no_promotions(
        self, promotion_repository, session
    ):
        # Arrange: No hay promociones en la base de datos
        query = PaginationQuery(page=1, page_size=10)

        page_result = await promotion_repository.get_active_promotions(query)

        assert len(page_result.items) == 0
        assert page_result.metadata.total_items == 0
        assert page_result.metadata.total_pages == 1
        assert page_result.metadata.current_page == 1
        assert page_result.metadata.items_per_page == 10

    @pytest.mark.asyncio
    async def test_get_active_promotions_multiple_active_promotions_single_page(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange: Crear 5 promociones activas
        for _ in range(5):
            promo_data = sample_promotion_data.copy()
            promo_data["start_date"] = datetime.now(timezone.utc) - timedelta(days=5)
            promo_data["end_date"] = datetime.now(timezone.utc) + timedelta(days=5)
            promo_data["is_active"] = True
            promotion = Promotion(**promo_data, id=PromotionId.generate())
            await promotion_repository.create(promotion)
        await session.commit()

        query = PaginationQuery(page=1, page_size=10)

        page_result = await promotion_repository.get_active_promotions(query)

        assert len(page_result.items) == 5
        assert page_result.metadata.total_items == 5
        assert page_result.metadata.total_pages == 1
        assert page_result.metadata.current_page == 1
        assert page_result.metadata.items_per_page == 10
        for promo in page_result.items:
            assert promo.is_active is True
            assert promo.start_date <= datetime.now(timezone.utc)
            assert promo.end_date >= datetime.now(timezone.utc)

    @pytest.mark.asyncio
    async def test_get_active_promotions_multiple_pages(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange: Crear 15 promociones activas para probar múltiples páginas
        expected_active_promotions = []
        for i in range(15):
            promo_data = sample_promotion_data.copy()
            promo_data["name"] = f"Active Promotion {i+1}"
            promo_data["start_date"] = datetime.now(timezone.utc) - timedelta(days=10)
            promo_data["end_date"] = datetime.now(timezone.utc) + timedelta(days=10)
            promo_data["is_active"] = True
            promotion = Promotion(**promo_data, id=PromotionId.generate())
            await promotion_repository.create(promotion)
            expected_active_promotions.append(promotion)
        await session.commit()

        query_page1 = PaginationQuery(page=1, page_size=5)
        page1 = await promotion_repository.get_active_promotions(query_page1)

        assert len(page1.items) == 5
        assert page1.metadata.total_items == 15
        assert page1.metadata.total_pages == 3
        assert page1.metadata.current_page == 1
        assert page1.metadata.items_per_page == 5
        assert set(p.id for p in page1.items) == set(
            p.id for p in expected_active_promotions[0:5]
        )

        query_page2 = PaginationQuery(page=2, page_size=5)
        page2 = await promotion_repository.get_active_promotions(query_page2)

        assert len(page2.items) == 5
        assert page2.metadata.total_items == 15
        assert page2.metadata.total_pages == 3
        assert page2.metadata.current_page == 2
        assert page2.metadata.items_per_page == 5
        assert set(p.id for p in page2.items) == set(
            p.id for p in expected_active_promotions[5:10]
        )

        query_page3 = PaginationQuery(page=3, page_size=5)
        page3 = await promotion_repository.get_active_promotions(query_page3)

        assert len(page3.items) == 5
        assert page3.metadata.total_items == 15
        assert page3.metadata.total_pages == 3
        assert page3.metadata.current_page == 3
        assert page3.metadata.items_per_page == 5
        assert set(p.id for p in page3.items) == set(
            p.id for p in expected_active_promotions[10:15]
        )

        query_page4 = PaginationQuery(page=4, page_size=5)
        page4 = await promotion_repository.get_active_promotions(query_page4)
        assert len(page4.items) == 0
        assert page4.metadata.total_items == 15
        assert page4.metadata.total_pages == 3
        assert page4.metadata.current_page == 4
        assert page4.metadata.items_per_page == 5

    @pytest.mark.asyncio
    async def test_get_active_promotions_with_inactive_promotions(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange: Crear promociones activas e inactivas
        # Activa
        active_promo_data = sample_promotion_data.copy()
        active_promo_data["start_date"] = datetime.now(timezone.utc) - timedelta(days=5)
        active_promo_data["end_date"] = datetime.now(timezone.utc) + timedelta(days=5)
        active_promo_data["is_active"] = True
        active_promotion = Promotion(**active_promo_data, id=PromotionId.generate())
        await promotion_repository.create(active_promotion)

        # Inactiva (is_active = False)
        inactive_promo_data_1 = sample_promotion_data.copy()
        inactive_promo_data_1["is_active"] = False
        inactive_promo_1 = Promotion(**inactive_promo_data_1, id=PromotionId.generate())
        await promotion_repository.create(inactive_promo_1)

        # Inactiva (fecha de inicio futura)
        inactive_promo_data_2 = sample_promotion_data.copy()
        inactive_promo_data_2["start_date"] = datetime.now(timezone.utc) + timedelta(
            days=1
        )
        inactive_promo_data_2["end_date"] = datetime.now(timezone.utc) + timedelta(
            days=30
        )
        inactive_promo_data_2["is_active"] = True  # Activa pero no en rango
        inactive_promo_2 = Promotion(**inactive_promo_data_2, id=PromotionId.generate())
        await promotion_repository.create(inactive_promo_2)

        # Inactiva (fecha de fin pasada)
        inactive_promo_data_3 = sample_promotion_data.copy()
        inactive_promo_data_3["start_date"] = datetime.now(timezone.utc) - timedelta(
            days=30
        )
        inactive_promo_data_3["end_date"] = datetime.now(timezone.utc) - timedelta(
            days=1
        )
        inactive_promo_data_3["is_active"] = True  # Activa pero no en rango
        inactive_promo_3 = Promotion(**inactive_promo_data_3, id=PromotionId.generate())
        await promotion_repository.create(inactive_promo_3)

        await session.commit()

        query = PaginationQuery(page=1, page_size=10)

        page_result = await promotion_repository.get_active_promotions(query)

        assert len(page_result.items) == 1
        assert page_result.items[0].id == active_promotion.id
        assert page_result.metadata.total_items == 1
        assert page_result.metadata.total_pages == 1
        assert page_result.metadata.current_page == 1
        assert page_result.metadata.items_per_page == 10

    @pytest.mark.asyncio
    async def test_get_active_promotions_database_error(
        self, promotion_repository, mocker
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError(
            "Database error during active promotions fetch"
        )

        repo = PromotionRepo(mock_session)
        query = PaginationQuery(page=1, page_size=10)

        with pytest.raises(DatabaseException):
            await repo.get_active_promotions(query)

    @pytest.mark.asyncio
    async def test_get_by_product_no_promotions_found(
        self, promotion_repository, session, sample_product
    ):
        # Arrange: Un producto existe, pero no hay promociones asociadas a él
        query = GetPromotionByProductIdQuery(
            product_id=sample_product.id, pagination=PaginationQuery()
        )

        page_result = await promotion_repository.get_by_product(query)

        assert len(page_result.items) == 0
        assert page_result.metadata.total_items == 0
        assert page_result.metadata.total_pages == 1
        assert page_result.metadata.current_page == 1
        assert page_result.metadata.items_per_page == 10

    @pytest.mark.asyncio
    async def test_get_by_product_single_page_active_promotions(
        self, promotion_repository, session, sample_product, sample_promotion_data
    ):
        # Arrange: Crear 3 promociones activas asociadas al producto
        expected_promotions = []
        for i in range(3):
            promo_data = sample_promotion_data.copy()
            promo_data["name"] = f"Promo for Prod {i+1}"
            promo_data["applicable_product_ids"] = [sample_product.id]
            promo_data["start_date"] = datetime.now(timezone.utc) - timedelta(days=5)
            promo_data["end_date"] = datetime.now(timezone.utc) + timedelta(days=5)
            promo_data["is_active"] = True
            promotion = Promotion(**promo_data, id=PromotionId.generate())
            await promotion_repository.create(promotion)
            expected_promotions.append(promotion)
        await session.commit()

        query = GetPromotionByProductIdQuery(
            product_id=sample_product.id, pagination=PaginationQuery(page_size=10)
        )

        page_result = await promotion_repository.get_by_product(query)

        assert len(page_result.items) == 3
        assert page_result.metadata.total_items == 3
        assert page_result.metadata.total_pages == 1
        assert page_result.metadata.current_page == 1
        assert page_result.metadata.items_per_page == 10
        retrieved_ids = {p.id for p in page_result.items}
        expected_ids = {p.id for p in expected_promotions}
        assert retrieved_ids == expected_ids
        for promo in page_result.items:
            assert promo.is_active is True
            assert promo.start_date <= datetime.now(timezone.utc)
            assert promo.end_date >= datetime.now(timezone.utc)

    @pytest.mark.asyncio
    async def test_create_promotion_no_products(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange
        promotion_id = PromotionId.generate()
        promo_data = sample_promotion_data.copy()
        promo_data["applicable_product_ids"] = []  # No products
        promotion = Promotion(**promo_data, id=promotion_id)

        # Act
        created_promotion = await promotion_repository.create(promotion)
        await session.commit()  # Commit para persistir y poder consultar

        # Assert
        assert created_promotion is not None
        assert created_promotion.id == promotion_id
        assert created_promotion.name == promotion.name
        assert created_promotion.is_active == True
        assert len(created_promotion.applicable_product_ids) == 0

        # Verify directly from DB
        retrieved_model = await session.get(PromotionModel, promotion_id.value)
        assert retrieved_model is not None
        assert retrieved_model.id == promotion_id.value
        assert len(retrieved_model.products) == 0  # No products associated in DB

    @pytest.mark.asyncio
    async def test_create_promotion_with_existing_products(
        self, promotion_repository, session, sample_promotion_data, sample_product
    ):
        # Arrange
        promotion_id = PromotionId.generate()
        promo_data = sample_promotion_data.copy()
        # Associate with the existing sample_product
        promo_data["applicable_product_ids"] = [sample_product.id]
        promotion = Promotion(**promo_data, id=promotion_id)

        # Act
        created_promotion = await promotion_repository.create(promotion)
        await session.commit()  # Commit para persistir y poder consultar

        # Assert
        assert created_promotion is not None
        assert created_promotion.id == promotion_id
        assert len(created_promotion.applicable_product_ids) == 1
        assert created_promotion.applicable_product_ids[0] == sample_product.id

        # Verify directly from DB
        retrieved_model = await session.get(PromotionModel, promotion_id.value)
        assert retrieved_model is not None
        assert retrieved_model.id == promotion_id.value
        assert len(retrieved_model.products) == 1  # One product associated
        assert retrieved_model.products[0].id == sample_product.id.value

    @pytest.mark.asyncio
    async def test_create_promotion_with_mixed_products_existing_and_non_existent(
        self,
        promotion_repository,
        session,
        sample_promotion_data,
        sample_product,
        caplog,
    ):
        # Arrange
        non_existent_product_id = (
            ProductId.generate()
        )  # This product will not be in the DB

        promotion_id = PromotionId.generate()
        promo_data = sample_promotion_data.copy()
        promo_data["applicable_product_ids"] = [
            sample_product.id,
            non_existent_product_id,
        ]
        promotion = Promotion(**promo_data, id=promotion_id)

        # Act
        with caplog.at_level(logging.WARNING):  # Capture warnings
            created_promotion = await promotion_repository.create(promotion)
            await session.commit()

        # Assert
        assert created_promotion is not None
        assert created_promotion.id == promotion_id
        # Only the existing product should be associated in the domain object
        assert len(created_promotion.applicable_product_ids) == 1
        assert created_promotion.applicable_product_ids[0] == sample_product.id

        # Verify directly from DB
        retrieved_model = await session.get(PromotionModel, promotion_id.value)
        assert retrieved_model is not None
        assert (
            len(retrieved_model.products) == 1
        )  # Only the existing product should be linked
        assert retrieved_model.products[0].id == sample_product.id.value

        # Verify warning message was logged
        assert any(
            f"Producto con ID {non_existent_product_id.value} no encontrado para la promoción {promotion_id.value}. No se asociará."
            in record.message
            for record in caplog.records
        )

    @pytest.mark.asyncio
    async def test_create_promotion_database_error(
        self, promotion_repository, mocker, sample_promotion_data
    ):
        # Arrange
        # Mock the session's add method to raise SQLAlchemyError
        mock_session = AsyncMock()
        mock_session.add = MagicMock(
            side_effect=SQLAlchemyError("Database error during add")
        )
        mock_session.execute.return_value = MagicMock(
            scalars=MagicMock(all=MagicMock(return_value=[]))
        )

        repo = PromotionRepo(mock_session)
        promotion_id = PromotionId.generate()
        promotion = Promotion(**sample_promotion_data, id=promotion_id)

        # Act & Assert
        with pytest.raises(DatabaseException) as excinfo:
            await repo.create(promotion)
        assert "Failed to create promotion" in str(excinfo.value)
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_promotion_success(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange: Create a promotion to be deleted
        promotion_id = PromotionId.generate()
        promotion = Promotion(**sample_promotion_data, id=promotion_id)
        await promotion_repository.create(promotion)
        await session.commit()

        # Verify it exists before deletion
        # Usar la sesión del test para verificar, no la del repositorio
        retrieved_model = await session.get(PromotionModel, promotion_id.value)
        assert retrieved_model is not None

        # Act
        deleted_successfully = await promotion_repository.delete(promotion_id)

        # Assert
        assert deleted_successfully is True
        session.expire_all()
        retrieved_model_after_delete = await session.get(
            PromotionModel, promotion_id.value
        )
        assert retrieved_model_after_delete is None

    @pytest.mark.asyncio
    async def test_delete_promotion_database_error(self, promotion_repository, mocker):
        # Arrange
        promotion_id = PromotionId.generate()

        mocker.patch.object(
            promotion_repository.session,
            "execute",
            side_effect=SQLAlchemyError("Database error during delete operation"),
        )

        # Act & Assert
        with pytest.raises(DatabaseException) as excinfo:
            await promotion_repository.delete(
                promotion_id
            )  # Llama al método que debería lanzar la excepción

        assert "Failed to delete promotion" in str(excinfo.value)
        assert isinstance(excinfo.value.__cause__, SQLAlchemyError)

    @pytest.mark.asyncio
    async def test_apply_promotion_use_success(
        self, promotion_repository, session, sample_promotion_data
    ):
        # Arrange: Create a promotion with initial current_uses = 0
        promotion_id = PromotionId.generate()
        promo_data = sample_promotion_data.copy()
        promo_data["current_uses"] = 0
        promotion = Promotion(**promo_data, id=promotion_id)
        await promotion_repository.create(promotion)
        await session.commit()

        # Verify initial uses
        initial_promotion_model = await session.get(PromotionModel, promotion_id.value)
        assert initial_promotion_model.current_uses == 0

        # Act
        applied_successfully = await promotion_repository.apply_promotion_use(
            promotion_id
        )

        # Assert
        assert applied_successfully is True
        # Verify uses incremented in DB
        session.expire_all()
        updated_promotion_model = await session.get(PromotionModel, promotion_id.value)
        assert updated_promotion_model.current_uses == 1

    @pytest.mark.asyncio
    async def test_apply_promotion_use_database_error(
        self, promotion_repository, mocker
    ):
        # Arrange
        promotion_id = PromotionId.generate()

        mocker.patch.object(
            promotion_repository.session,
            "execute",
            side_effect=SQLAlchemyError("Database error during update operation"),
        )

        # Act & Assert
        with pytest.raises(DatabaseException) as excinfo:
            await promotion_repository.apply_promotion_use(promotion_id)

        assert "Failed to apply promotion use" in str(excinfo.value)
        assert isinstance(excinfo.value.__cause__, SQLAlchemyError)
