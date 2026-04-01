from typing import List

from app.payments.domain.entities import StoredPaymentMethod
from app.payments.domain.interfaces import PaymentEventsPublisher, StoredPaymentMethodRepository
from app.payments.domain.value_objects import Card
from app.payments.application.commands import (
    CreateStoredPaymentMethodCommand,
    SoftDeleteStoredPaymentMethodCommand,
)
from app.shared.base_exceptions import NotFoundException


async def _publish_stored_events(
    publisher: PaymentEventsPublisher, entity: StoredPaymentMethod
) -> None:
    for ev in entity.get_events():
        await publisher.publish(
            event_name=ev.event_type(),
            key=entity.user_id,
            payload=ev.to_dict(),
        )
    entity.clear_events()


class CreateStoredPaymentMethodUseCase:
    def __init__(
        self,
        stored_repo: StoredPaymentMethodRepository,
        events_publisher: PaymentEventsPublisher,
    ) -> None:
        self._stored_repo = stored_repo
        self._events_publisher = events_publisher

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
        entity = StoredPaymentMethod.create(
            user_id=command.user_id,
            card=card,
            is_default=command.is_default,
        )
        saved = await self._stored_repo.save(entity)
        await _publish_stored_events(self._events_publisher, entity)
        return saved


class ListStoredPaymentMethodsQuery:
    def __init__(self, stored_repo: StoredPaymentMethodRepository) -> None:
        self._stored_repo = stored_repo

    async def execute(self, user_id: str) -> List[StoredPaymentMethod]:
        return await self._stored_repo.list_for_user(user_id)


class SoftDeleteStoredPaymentMethodUseCase:
    def __init__(
        self,
        stored_repo: StoredPaymentMethodRepository,
        events_publisher: PaymentEventsPublisher,
    ) -> None:
        self._stored_repo = stored_repo
        self._events_publisher = events_publisher

    async def execute(self, user_id: str, command: SoftDeleteStoredPaymentMethodCommand) -> None:
        entity = await self._stored_repo.get_for_user(command.id, user_id)
        if not entity:
            raise NotFoundException("StoredPaymentMethod", command.id, id_name="payment method id")
        entity.delete()
        await self._stored_repo.save(entity)
        await _publish_stored_events(self._events_publisher, entity)
