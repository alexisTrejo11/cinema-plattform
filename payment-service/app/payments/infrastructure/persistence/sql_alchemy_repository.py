from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.payments.domain.entities import Payment, PaymentMethod
from app.payments.domain.value_objects import PaymentId
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.interfaces import PaymentRepository, PaymentMethodRepository

from .models import PaymentModel, PaymentMethodModel
from .model_mapper import ModelMapper


def _payment_method_to_row(entity: PaymentMethod) -> PaymentMethodModel:
    """Domain → ORM; enums persisted as their string values."""
    return PaymentMethodModel(
        id=entity.id,
        name=entity.name,
        provider=entity.provider.value,
        type=entity.type.value,
        stripe_code=entity.stripe_code,
        is_active=entity.is_active,
        min_amount=Decimal(str(entity.min_amount)),
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        deleted_at=entity.deleted_at,
    )


class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, payment_id: PaymentId) -> Optional[Payment]:
        stmt = select(PaymentModel).where(PaymentModel.id == str(payment_id.value))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return ModelMapper.model_to_entity(model) if model else None

    async def list(self, criteria: PaymentListCriteria) -> List[Payment]:
        stmt = select(PaymentModel)
        if criteria.user_id:
            stmt = stmt.where(PaymentModel.user_id == criteria.user_id)
        if criteria.status:
            stmt = stmt.where(PaymentModel.status == criteria.status)
        stmt = stmt.limit(criteria.limit).offset(criteria.offset)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [ModelMapper.model_to_entity(model) for model in models]

    async def save(self, payment: Payment) -> Payment:
        payment_model = ModelMapper.entity_to_model(payment)
        if not payment.id:
            self.session.add(payment_model)
            await self.session.flush()
        else:
            await self.session.merge(payment_model)

        await self.session.commit()
        await self.session.refresh(payment_model)

        return ModelMapper.model_to_entity(payment_model)

    async def delete(self, payment_id: PaymentId) -> bool:
        stmt = select(PaymentModel).where(PaymentModel.id == str(payment_id.value))
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        await self.session.delete(model)
        await self.session.commit()
        return True


class SqlAlchemyPaymentMethodRepository(PaymentMethodRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(
        self, payment_method_id: str, include_deleted: bool = False
    ) -> Optional[PaymentMethod]:
        """Find a payment method by its ID."""

        stmt = select(PaymentMethodModel).where(
            PaymentMethodModel.id == payment_method_id,
        )
        if not include_deleted:
            stmt = stmt.where(PaymentMethodModel.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PaymentMethod.model_validate(model) if model else None

    async def find_all(self) -> List[PaymentMethod]:
        """Find all non-deleted payment methods."""
        stmt = select(PaymentMethodModel).where(
            PaymentMethodModel.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return [PaymentMethod.model_validate(row) for row in result.scalars().all()]

    async def save(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Insert or update by primary key (includes soft-deleted rows → update)."""
        if await self._row_exists(payment_method.id):
            return await self._update(payment_method)
        return await self._create(payment_method)

    async def _create(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Create a payment method."""
        row = _payment_method_to_row(payment_method)
        self.session.add(row)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(row)
        return PaymentMethod.model_validate(row)

    async def _update(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Update a payment method."""
        row = _payment_method_to_row(payment_method)
        merged = await self.session.merge(row)
        await self.session.commit()
        await self.session.refresh(merged)
        return PaymentMethod.model_validate(merged)

    async def _row_exists(self, payment_method_id: str) -> bool:
        """True if any row exists for this id (deleted or not)."""
        stmt = select(PaymentMethodModel.id).where(
            PaymentMethodModel.id == payment_method_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def delete(self, payment_method_id: str) -> bool:
        """Hard-delete a payment method row."""
        stmt = select(PaymentMethodModel).where(
            PaymentMethodModel.id == payment_method_id,
            PaymentMethodModel.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        await self.session.delete(model)
        await self.session.commit()

        return True
