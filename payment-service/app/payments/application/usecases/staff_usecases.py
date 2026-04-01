from typing import Any

from app.payments.domain.entities import Payment
from app.payments.domain.exceptions import PaymentNotRefundableException
from app.payments.domain.interfaces import PaymentEventsPublisher, PaymentRepository
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.value_objects import PaymentId, PaymentStatus
from app.shared.base_exceptions import NotFoundException


class StaffPaymentUseCases:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        events_publisher: PaymentEventsPublisher,
    ) -> None:
        self.payment_repository = payment_repository
        self.events_publisher = events_publisher

    async def verify_payment_status(self, payment_id: str) -> Payment:
        payment = await self.payment_repository.get_by_id(PaymentId.from_string(payment_id))
        if not payment:
            raise NotFoundException("Payment", payment_id, id_name="payment id")
        return payment

    async def get_receipt(self, payment_id: str) -> dict[str, Any]:
        payment = await self.verify_payment_status(payment_id)
        return {
            "payment_id": str(payment.id.value),
            "status": payment.status.value,
            "amount": payment.amount.to_float(),
            "currency": payment.amount.currency.value,
            "issued_at": payment.completed_at or payment.updated_at,
            "receipt_url": f"https://payments.local/receipts/{payment.id.value}",
        }

    async def refund_for_cancelled_show(self, payment_id: str, reason: str) -> Payment:
        payment = await self.verify_payment_status(payment_id)
        if not payment.can_be_refunded():
            raise PaymentNotRefundableException(str(payment.id), "Payment is not refundable")

        payment.refund(
            refund_amount=payment.get_remaining_refundable_amount(),
            reason=reason,
            transaction_reference=f"rf_staff_{payment.id.value.hex[:16]}",
        )
        saved = await self.payment_repository.save(payment)
        await self.events_publisher.publish(
            event_name="payment.refund.staff_requested",
            key=str(saved.id.value),
            payload={"payment_id": str(saved.id.value), "reason": reason},
        )
        return saved

    async def get_payments_by_show(
        self, show_id: str, limit: int = 100, offset: int = 0
    ) -> list[Payment]:
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=limit, offset=offset)
        )
        return [
            payment
            for payment in payments
            if payment.metadata and payment.metadata.show_id == show_id
        ]

    async def get_show_revenue_summary(self, show_id: str) -> dict[str, Any]:
        payments = await self.get_payments_by_show(show_id)
        completed = [
            p
            for p in payments
            if p.status in (PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED)
        ]
        gross = sum(p.amount.to_float() for p in completed)
        refunded = sum(
            (p.refunded_amount.to_float() if p.refunded_amount else 0.0)
            for p in completed
        )
        return {
            "show_id": show_id,
            "payments_count": len(payments),
            "completed_count": len(completed),
            "gross_revenue": gross,
            "refunded_revenue": refunded,
            "net_revenue": gross - refunded,
            "currency": completed[0].amount.currency.value if completed else "USD",
        }

    async def handle_stripe_webhook(
        self, event_type: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        # Placeholder until Stripe signature validation and robust mapping are added.
        await self.events_publisher.publish(
            event_name=f"stripe.webhook.{event_type}",
            key=payload.get("id"),
            payload=payload,
        )
        return {"received": True, "event_type": event_type}
