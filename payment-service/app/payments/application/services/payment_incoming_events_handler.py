from __future__ import annotations

from typing import Any

from app.payments.domain.interfaces import PaymentEventsPublisher, PaymentRepository
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.value_objects import PaymentId


class PaymentIncomingEventsHandler:
    """
    Handles external integration events consumed from Kafka.

    Keep mappings intentionally small and explicit; add new event types as
    contracts stabilize across services.
    """

    def __init__(
        self,
        payment_repository: PaymentRepository,
        events_publisher: PaymentEventsPublisher,
    ) -> None:
        self.payment_repository = payment_repository
        self.events_publisher = events_publisher

    async def handle(self, envelope: dict[str, Any]) -> None:
        event_type = str(envelope.get("event_type") or "").strip()
        payload = envelope.get("payload") or {}
        if not event_type:
            return

        if event_type in {"payment.external.confirmed", "stripe.payment_intent.succeeded"}:
            await self._mark_payment_completed(payload)
            return

        if event_type in {"payment.external.failed", "stripe.payment_intent.failed"}:
            await self._mark_payment_failed(payload)
            return

        if event_type == "show.cancelled":
            await self._handle_show_cancelled(payload)
            return

    async def _mark_payment_completed(self, payload: dict[str, Any]) -> None:
        payment_id = payload.get("payment_id")
        if not payment_id:
            return
        payment = await self.payment_repository.get_by_id(PaymentId.from_string(payment_id))
        if not payment:
            return
        if payment.can_be_completed():
            payment.complete(transaction_reference=payload.get("transaction_reference"))
            saved = await self.payment_repository.save(payment)
            await self.events_publisher.publish(
                event_name="payment.completed",
                key=str(saved.id.value),
                payload={"payment_id": str(saved.id.value), "source": "incoming_kafka"},
            )

    async def _mark_payment_failed(self, payload: dict[str, Any]) -> None:
        payment_id = payload.get("payment_id")
        if not payment_id:
            return
        payment = await self.payment_repository.get_by_id(PaymentId.from_string(payment_id))
        if not payment:
            return
        if payment.status.value not in {"completed", "refunded", "cancelled"}:
            payment.fail(reason=str(payload.get("reason") or "External payment failed"))
            saved = await self.payment_repository.save(payment)
            await self.events_publisher.publish(
                event_name="payment.failed",
                key=str(saved.id.value),
                payload={"payment_id": str(saved.id.value), "source": "incoming_kafka"},
            )

    async def _handle_show_cancelled(self, payload: dict[str, Any]) -> None:
        show_id = payload.get("show_id")
        if not show_id:
            return
        # Keep it simple: scan recent payments and refund matching show payments.
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        for payment in payments:
            if not payment.metadata or payment.metadata.show_id != show_id:
                continue
            if not payment.can_be_refunded():
                continue
            payment.refund(
                refund_amount=payment.get_remaining_refundable_amount(),
                reason="Auto refund due to cancelled show",
                transaction_reference=f"rf_auto_{payment.id.value.hex[:12]}",
            )
            saved = await self.payment_repository.save(payment)
            await self.events_publisher.publish(
                event_name="payment.refunded",
                key=str(saved.id.value),
                payload={
                    "payment_id": str(saved.id.value),
                    "show_id": show_id,
                    "source": "incoming_kafka",
                },
            )
