from collections import Counter
from typing import Any

from app.payments.domain.entities import Payment
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.exceptions import PaymentNotRefundableException
from app.payments.domain.interfaces import PaymentEventsPublisher, PaymentRepository
from app.payments.domain.value_objects import Money, PaymentId, PaymentStatus
from app.shared.base_exceptions import NotFoundException, ValidationException


class AdminPaymentUseCases:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        events_publisher: PaymentEventsPublisher,
    ) -> None:
        self.payment_repository = payment_repository
        self.events_publisher = events_publisher

    async def search_payments(self, criteria: PaymentListCriteria) -> list[Payment]:
        return await self.payment_repository.list(criteria)

    async def get_payment_detail(self, payment_id: str) -> Payment:
        payment = await self.payment_repository.get_by_id(PaymentId.from_string(payment_id))
        if not payment:
            raise NotFoundException("Payment", payment_id, id_name="payment id")
        return payment

    async def override_payment_status(self, payment_id: str, status: str) -> Payment:
        payment = await self.get_payment_detail(payment_id)
        try:
            target = PaymentStatus(status)
        except ValueError as exc:
            raise ValidationException("status", f"Unsupported status '{status}'") from exc

        if target == PaymentStatus.COMPLETED:
            payment.complete(transaction_reference=f"tx_admin_{payment.id.value.hex[:12]}")
        elif target == PaymentStatus.CANCELLED:
            payment.cancel(reason="Overridden by admin")
        elif target == PaymentStatus.FAILED:
            payment.fail(reason="Marked as failed by admin")
        else:
            payment.status = target

        saved = await self.payment_repository.save(payment)
        await self.events_publisher.publish(
            event_name="payment.status.overridden",
            key=str(saved.id.value),
            payload={"payment_id": str(saved.id.value), "status": saved.status.value},
        )
        return saved

    async def force_refund(
        self, payment_id: str, reason: str, refund_amount: float | None = None
    ) -> Payment:
        payment = await self.get_payment_detail(payment_id)
        if not payment.can_be_refunded():
            raise PaymentNotRefundableException(str(payment.id), "Payment is not refundable")

        amount = (
            payment.get_remaining_refundable_amount()
            if refund_amount is None
            else Money.from_float(refund_amount, payment.amount.currency)
        )
        payment.refund(
            refund_amount=amount,
            reason=reason,
            transaction_reference=f"rf_admin_{payment.id.value.hex[:12]}",
        )
        saved = await self.payment_repository.save(payment)
        return saved

    async def void_payment(self, payment_id: str, reason: str) -> Payment:
        payment = await self.get_payment_detail(payment_id)
        payment.cancel(reason=reason)
        return await self.payment_repository.save(payment)

    async def list_transactions(self, criteria: PaymentListCriteria) -> list[dict[str, Any]]:
        # Placeholder until a transaction repository is implemented.
        payments = await self.payment_repository.list(criteria)
        return [
            {
                "id": str(p.id.value),
                "payment_id": str(p.id.value),
                "status": p.status.value,
                "amount": p.amount.to_float(),
                "currency": p.amount.currency.value,
                "created_at": p.created_at,
            }
            for p in payments
        ]

    async def get_transaction(self, transaction_id: str) -> dict[str, Any]:
        # Placeholder lookup through payment IDs for now.
        payment = await self.get_payment_detail(transaction_id)
        return {
            "id": str(payment.id.value),
            "payment_id": str(payment.id.value),
            "status": payment.status.value,
            "amount": payment.amount.to_float(),
            "currency": payment.amount.currency.value,
            "created_at": payment.created_at,
        }

    async def reverse_transaction(self, transaction_id: str, reason: str) -> dict[str, Any]:
        await self.events_publisher.publish(
            event_name="transaction.reverse.requested",
            key=transaction_id,
            payload={"transaction_id": transaction_id, "reason": reason},
        )
        return {"transaction_id": transaction_id, "status": "reverse_requested"}

    async def get_payments_summary(self) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        counter = Counter(p.status.value for p in payments)
        return {
            "total": len(payments),
            "by_status": dict(counter),
            "gross_amount": sum(p.amount.to_float() for p in payments),
        }

    async def get_summary_by_type(self) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        totals: dict[str, float] = {}
        for payment in payments:
            key = payment.payment_type.value
            totals[key] = totals.get(key, 0.0) + payment.amount.to_float()
        return totals

    async def get_summary_by_payment_method(self) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        totals: dict[str, float] = {}
        for payment in payments:
            key = payment.payment_method.value
            totals[key] = totals.get(key, 0.0) + payment.amount.to_float()
        return totals

    async def get_failed_payments_summary(self) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria(
                status=PaymentStatus.FAILED.value,
                limit=500,
                offset=0,
            )
        )
        return {
            "failed_count": len(payments),
            "failed_amount": sum(p.amount.to_float() for p in payments),
        }

    async def get_refunds_summary(self) -> dict[str, Any]:
        payments = await self.payment_repository.list(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        refunded = [
            payment
            for payment in payments
            if payment.status in (PaymentStatus.REFUNDED, PaymentStatus.PARTIALLY_REFUNDED)
        ]
        return {
            "refund_count": len(refunded),
            "refund_amount": sum(
                (p.refunded_amount.to_float() if p.refunded_amount else 0.0)
                for p in refunded
            ),
        }

    async def get_transactions_summary(self) -> dict[str, Any]:
        txs = await self.list_transactions(
            PaymentListCriteria.paginate(limit=500, offset=0)
        )
        return {"total_transactions": len(txs)}
