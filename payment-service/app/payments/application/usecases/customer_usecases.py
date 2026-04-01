from typing import Any

from app.payments.application.commands import (
    CreateStoredPaymentMethodCommand,
    ProcessPayCommand,
    SoftDeleteStoredPaymentMethodCommand,
)
from app.payments.domain.entities import Payment, StoredPaymentMethod
from app.payments.domain.events import DomainEvent
from app.payments.domain.exceptions import PaymentNotRefundableException
from app.payments.domain.interfaces import (
    PaymentEventsPublisher,
    PaymentRepository,
    PurchaseAssertionClient,
    StoredPaymentMethodRepository,
)
from app.payments.application.usecases.customer_store_method_usecases import (
    CreateStoredPaymentMethodUseCase,
    ListStoredPaymentMethodsQuery,
    SoftDeleteStoredPaymentMethodUseCase,
)
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.value_objects import (
    Currency,
    Money,
    PaymentId,
    PaymentMetadata,
    PaymentMethod,
    PaymentStatus,
    PaymentType,
    UserId,
)
from app.shared.base_exceptions import NotFoundException


def _stored_payment_method_to_api_row(spm: StoredPaymentMethod) -> dict[str, Any]:
    last4 = spm.card.card_number[-4:] if spm.card and len(spm.card.card_number) >= 4 else ""
    return {
        "id": spm.id,
        "user_id": spm.user_id,
        "last4": last4,
        "brand": "card",
        "is_default": spm.is_default,
        "created_at": spm.created_at,
    }


class CustomerPaymentUseCases:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        purchase_assertion_client: PurchaseAssertionClient,
        events_publisher: PaymentEventsPublisher,
        stored_payment_method_repository: StoredPaymentMethodRepository,
    ) -> None:
        self.payment_repository = payment_repository
        self.purchase_assertion_client = purchase_assertion_client
        self.events_publisher = events_publisher
        self._create_stored_pm = CreateStoredPaymentMethodUseCase(
            stored_payment_method_repository, events_publisher
        )
        self._list_stored_pm = ListStoredPaymentMethodsQuery(stored_payment_method_repository)
        self._delete_stored_pm = SoftDeleteStoredPaymentMethodUseCase(
            stored_payment_method_repository, events_publisher
        )

    async def get_payment_history(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[Payment]:
        return await self.payment_repository.list(
            PaymentListCriteria(user_id=user_id, limit=limit, offset=offset)
        )

    async def get_payment_detail(self, user_id: str, payment_id: str) -> Payment:
        payment = await self.payment_repository.get_by_id(PaymentId.from_string(payment_id))
        if not payment or str(payment.user_id) != user_id:
            raise NotFoundException("Payment", payment_id, id_name="payment id")
        return payment

    async def get_payment_summary(self, user_id: str) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria(user_id=user_id, limit=200, offset=0)
        )
        total_paid = sum(
            p.amount.to_float()
            for p in payments
            if p.status in (PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED)
        )
        total_refunded = sum(
            (p.refunded_amount.to_float() if p.refunded_amount else 0.0) for p in payments
        )
        return {
            "total_payments": len(payments),
            "completed_payments": len(
                [p for p in payments if p.status == PaymentStatus.COMPLETED]
            ),
            "failed_payments": len([p for p in payments if p.status == PaymentStatus.FAILED]),
            "total_paid_amount": total_paid,
            "total_refunded_amount": total_refunded,
            "currency": payments[0].amount.currency.value if payments else Currency.USD.value,
        }

    async def get_receipt(self, user_id: str, payment_id: str) -> dict[str, Any]:
        payment = await self.get_payment_detail(user_id=user_id, payment_id=payment_id)
        return {
            "payment_id": str(payment.id.value),
            "status": payment.status.value,
            "amount": payment.amount.to_float(),
            "currency": payment.amount.currency.value,
            "issued_at": payment.completed_at or payment.updated_at,
            "receipt_url": f"https://payments.local/receipts/{payment.id.value}",
        }

    async def initiate_payment(self, user_id: str, payment_id: str) -> dict[str, Any]:
        payment = await self.get_payment_detail(user_id=user_id, payment_id=payment_id)
        payment.start_processing()
        payment.stripe_payment_intent_id = payment.stripe_payment_intent_id or (
            f"pi_placeholder_{payment.id.value.hex[:16]}"
        )
        await self.payment_repository.save(payment)
        await self._publish_payment_events(payment)
        return {
            "payment_id": str(payment.id.value),
            "status": payment.status.value,
            "stripe_payment_intent_id": payment.stripe_payment_intent_id,
            "client_secret": f"{payment.stripe_payment_intent_id}_secret_placeholder",
        }

    async def confirm_payment(self, user_id: str, payment_id: str) -> Payment:
        payment = await self.get_payment_detail(user_id=user_id, payment_id=payment_id)
        payment.complete(transaction_reference=f"tx_{payment.id.value.hex[:16]}")
        saved = await self.payment_repository.save(payment)
        await self._publish_payment_events(saved)
        return saved

    async def cancel_payment(self, user_id: str, payment_id: str, reason: str) -> Payment:
        payment = await self.get_payment_detail(user_id=user_id, payment_id=payment_id)
        payment.cancel(reason=reason)
        saved = await self.payment_repository.save(payment)
        await self._publish_payment_events(saved)
        return saved

    async def request_refund(
        self, user_id: str, payment_id: str, reason: str, refund_amount: float | None = None
    ) -> Payment:
        payment = await self.get_payment_detail(user_id=user_id, payment_id=payment_id)
        if not payment.can_be_refunded():
            raise PaymentNotRefundableException(str(payment.id), "Payment is not refundable")

        amount = (
            Money.from_float(refund_amount, payment.amount.currency)
            if refund_amount is not None
            else payment.get_remaining_refundable_amount()
        )
        payment.refund(
            refund_amount=amount,
            reason=reason,
            transaction_reference=f"rf_{payment.id.value.hex[:16]}",
        )
        saved = await self.payment_repository.save(payment)
        await self._publish_payment_events(saved)
        return saved

    async def purchase_tickets(self, command: ProcessPayCommand) -> Payment:
        await self.purchase_assertion_client.assert_ticket_purchase(
            str(command.user_id), command.metadata or {}
        )
        return await self._create_purchase_intent(command, PaymentType.TICKET_PURCHASE)

    async def purchase_concessions(self, command: ProcessPayCommand) -> Payment:
        await self.purchase_assertion_client.assert_concessions_purchase(
            str(command.user_id), command.metadata or {}
        )
        return await self._create_purchase_intent(command, PaymentType.FOOD_PURCHASE)

    async def purchase_merchandise(self, command: ProcessPayCommand) -> Payment:
        await self.purchase_assertion_client.assert_merchandise_purchase(
            str(command.user_id), command.metadata or {}
        )
        return await self._create_purchase_intent(command, PaymentType.MERCHANDISE_PURCHASE)

    async def purchase_subscriptions(self, command: ProcessPayCommand) -> Payment:
        await self.purchase_assertion_client.assert_subscription_purchase(
            str(command.user_id), command.metadata or {}
        )
        return await self._create_purchase_intent(command, PaymentType.SUBSCRIPTION)

    async def purchase_wallet_credit(self, command: ProcessPayCommand) -> Payment:
        await self.purchase_assertion_client.assert_wallet_credit(
            str(command.user_id), command.metadata or {}
        )
        return await self._create_purchase_intent(command, PaymentType.WALLET_TOPUP)

    async def create_customer_stored_payment_method(
        self, command: CreateStoredPaymentMethodCommand
    ) -> dict[str, Any]:
        created = await self._create_stored_pm.execute(command)
        return _stored_payment_method_to_api_row(created)

    async def list_customer_stored_payment_methods(self, user_id: str) -> list[dict[str, Any]]:
        rows = await self._list_stored_pm.execute(user_id)
        return [_stored_payment_method_to_api_row(r) for r in rows]

    async def delete_customer_stored_payment_method(
        self, user_id: str, payment_method_id: str
    ) -> None:
        await self._delete_stored_pm.execute(
            user_id, SoftDeleteStoredPaymentMethodCommand(id=payment_method_id)
        )

    async def _create_purchase_intent(
        self, command: ProcessPayCommand, payment_type: PaymentType
    ) -> Payment:
        metadata = PaymentMetadata.model_validate(command.metadata or {})
        payment = Payment.create(
            user_id=UserId.from_string(str(command.user_id)),
            amount=Money.from_float(command.amount, Currency(command.currency)),
            payment_method=PaymentMethod(command.payment_method),
            payment_type=payment_type,
            metadata=metadata,
        )
        saved = await self.payment_repository.save(payment)
        await self.events_publisher.publish(
            event_name="payment.intent.created",
            key=str(saved.id.value),
            payload={
                "payment_id": str(saved.id.value),
                "user_id": str(saved.user_id.value),
                "amount": saved.amount.to_float(),
                "currency": saved.amount.currency.value,
                "payment_type": saved.payment_type.value,
                "metadata": saved.metadata.model_dump(mode="json") if saved.metadata else {},
            },
        )
        return saved

    async def _publish_payment_events(self, payment: Payment) -> None:
        events: list[DomainEvent] = payment.get_events()
        for event in events:
            await self.events_publisher.publish(
                event_name=event.event_type(),
                key=str(payment.id.value),
                payload=event.to_dict(),
            )
        payment.clear_events()
