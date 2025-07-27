from tests.repository.fixture.combos_fixtures import *
from app.shared.base_exceptions import DatabaseException
from sqlalchemy.exc import SQLAlchemyError


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
        assert retrieved_promotion.discount_value == promotion.discount_value
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
        promotion_data['is_active'] = False
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
        promotion_data['applicable_product_ids'] = [sample_product.id]
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
        mock_session = mocker.MagicMock()
        mock_session.execute.side_effect = SQLAlchemyError("Database error")
        repo = PromotionRepo(mock_session)
        test_id = PromotionId.generate()

        # Act & Assert
        with pytest.raises(DatabaseException):
            await repo.get_by_id(test_id)
