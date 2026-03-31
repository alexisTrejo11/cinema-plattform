from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.payments.domain.entities import Payment
from app.payments.domain.value_objects import PaymentId
from app.payments.domain.interfaces import PaymentRepository

from .models import PaymentModel
from .model_mapper import ModelMapper


class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, payment_id: PaymentId) -> Optional[Payment]:
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id.__str__)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return ModelMapper.model_to_entity(model) if model else None

    # TODO: Add filtering
    async def list(self, **kwargs) -> List[Payment]:
        stmt = select(PaymentModel)
        stmt.limit(10).offset(0)

        result = await self.session.execute(stmt)
        models = result.scalars()

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
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id.__str__)
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        await self.session.delete(model)
        await self.session.commit()
        return True
