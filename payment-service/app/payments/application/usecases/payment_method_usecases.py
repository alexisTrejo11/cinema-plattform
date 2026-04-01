from typing import List

from app.payments.application.commands import (
    CreatePaymentMethodCommand,
    UpdatePaymentMethodCommand,
)
from app.payments.domain.entities import PaymentMethod
from app.payments.domain.exceptions import PaymentMethodNotFoundException
from app.payments.domain.interfaces import PaymentMethodRepository


class PaymentMethodUseCases:
    def __init__(self, payment_method_repository: PaymentMethodRepository):
        self.payment_method_repository = payment_method_repository

    async def get_payment_method(self, id: str) -> PaymentMethod:
        payment_method = await self.payment_method_repository.find_by_id(id)
        if not payment_method:
            raise PaymentMethodNotFoundException(id)
        return payment_method

    async def get_all_payment_methods(self) -> List[PaymentMethod]:
        return await self.payment_method_repository.find_all()

    async def create_payment_method(
        self, command: CreatePaymentMethodCommand
    ) -> PaymentMethod:
        payment_method = PaymentMethod.create(**command.model_dump())
        return await self.payment_method_repository.save(payment_method)

    async def update_payment_method(self, command: UpdatePaymentMethodCommand) -> None:
        current_data = await self.payment_method_repository.find_by_id(command.id)
        if not current_data:
            raise PaymentMethodNotFoundException(command.id)

        update_data = command.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"id", "created_at", "updated_at", "deleted_at"},
        )
        updated_payment_method = current_data.update(update_data)
        await self.payment_method_repository.save(updated_payment_method)

    async def restore_payment_method(self, id: str) -> None:
        payment_method = await self.payment_method_repository.find_by_id(
            id, include_deleted=True
        )
        if not payment_method:
            raise PaymentMethodNotFoundException(id)

        await self.payment_method_repository.save(payment_method.mark_as_active())

    async def delete_payment_method(self, id: str, hard_delete: bool = False) -> None:
        payment_method = await self.payment_method_repository.find_by_id(id)
        if not payment_method:
            raise PaymentMethodNotFoundException(id)

        if hard_delete:
            await self.payment_method_repository.delete(id)
            return

        await self.payment_method_repository.save(payment_method.mark_as_deleted())
