from typing import List

from app.payments.domain.entities import StoredPaymentMethod
from app.payments.domain.value_objects import Card, UserId
from app.payments.application.commands import (
    CreateStoredPaymentMethodCommand,
    SoftDeleteStoredPaymentMethodCommand,
)


class CreateStoredPaymentMethodUseCase:
    def __init__(self, payment_method_repository):
        self.payment_method_repository = payment_method_repository

    async def execute(
        self, command: CreateStoredPaymentMethodCommand
    ) -> StoredPaymentMethod:
        card = Card(
            card_holder=command.card_holder,
            card_number=command.card_number,
            cvv=command.cvv,
            expiration_month=command.expiration_month,
            expiration_year=command.expiration_year,
            stripe_payment_method_id=command.stripe_payment_method_id,
        )

        payment_method = StoredPaymentMethod.create(
            user_id=UserId.from_string(command.user_id),
            card=card,
            is_default=command.is_default,
        )

        return await self.payment_method_repository.create(payment_method)


class ListStoredPaymentMethodsQuery:
    def __init__(self, payment_method_repository):
        self.payment_method_repository = payment_method_repository

    async def execute(self) -> List[StoredPaymentMethod]:
        return await self.payment_method_repository.find_all()


class SoftDeleteStoredPaymentMethodUseCase:
    def __init__(self, payment_method_repository):
        self.payment_method_repository = payment_method_repository

    async def execute(self, command: SoftDeleteStoredPaymentMethodCommand) -> None:
        payment_method = await self.payment_method_repository.find_by_id(command.id)

        if not payment_method:
            raise ValueError("Payment method not found")

        payment_method.delete()

        await self.payment_method_repository.update(payment_method)
