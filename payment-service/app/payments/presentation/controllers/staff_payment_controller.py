from typing import Any, List

from fastapi import APIRouter, Depends, Query

from app.payments.application.usecases.staff_usecases import StaffPaymentUseCases
from app.payments.presentation.depencies import get_staff_payment_use_cases
from app.payments.presentation.dtos import (
    PaymentResponse,
    ReceiptResponse,
    StaffRefundRequest,
    StripeWebhookRequest,
)
from app.shared.auth import require_staff_user

router = APIRouter(prefix="/api/v1/payments/staff", tags=["Staff - Payments"])


@router.get("/{payment_id}/status", response_model=PaymentResponse)
async def verify_payment_status(
    payment_id: str,
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.verify_payment_status(payment_id)
    return PaymentResponse.from_entity(payment)


@router.get("/{payment_id}/receipt", response_model=ReceiptResponse)
async def get_receipt(
    payment_id: str,
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> ReceiptResponse:
    receipt = await use_case.get_receipt(payment_id)
    return ReceiptResponse(**receipt)


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_for_cancelled_show(
    payment_id: str,
    body: StaffRefundRequest,
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.refund_for_cancelled_show(payment_id, body.reason)
    return PaymentResponse.from_entity(payment)


@router.get("/show/{show_id}", response_model=List[PaymentResponse])
async def get_payments_by_show(
    show_id: str,
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> List[PaymentResponse]:
    payments = await use_case.get_payments_by_show(show_id, limit=limit, offset=offset)
    return [PaymentResponse.from_entity(payment) for payment in payments]


@router.get("/show/{show_id}/summary")
async def get_show_revenue_summary(
    show_id: str,
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> dict:
    return await use_case.get_show_revenue_summary(show_id)


@router.post("/stripe")
async def stripe_webhook(
    body: StripeWebhookRequest,
    _: Any = Depends(require_staff_user),
    use_case: StaffPaymentUseCases = Depends(get_staff_payment_use_cases),
) -> dict:
    return await use_case.handle_stripe_webhook(body.event_type, body.payload)
