from typing import Any, List

from fastapi import APIRouter, Depends

from app.payments.application.usecases.admin_usecases import AdminPaymentUseCases
from app.payments.presentation.depencies import get_admin_payment_use_cases
from app.payments.presentation.dtos import (
    AdminOverrideStatusRequest,
    AdminPaginationQuery,
    AdminPaymentSearchQuery,
    AdminRefundRequest,
    AdminVoidRequest,
    PaymentResponse,
    ReverseTransactionRequest,
)
from app.shared.auth import require_admin_user

router = APIRouter(prefix="/api/v1/payments/admin", tags=["Admin - Payments"])


@router.get("/payments", response_model=List[PaymentResponse])
async def search_payments(
    query: AdminPaymentSearchQuery = Depends(),
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> List[PaymentResponse]:
    payments = await use_case.search_payments(query.to_criteria())
    return [PaymentResponse.from_entity(payment) for payment in payments]


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment_detail(
    payment_id: str,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.get_payment_detail(payment_id)
    return PaymentResponse.from_entity(payment)


@router.patch("/payments/{payment_id}/status", response_model=PaymentResponse)
async def override_payment_status(
    payment_id: str,
    body: AdminOverrideStatusRequest,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.override_payment_status(payment_id, body.status)
    return PaymentResponse.from_entity(payment)


@router.post("/payments/{payment_id}/refund", response_model=PaymentResponse)
async def force_refund(
    payment_id: str,
    body: AdminRefundRequest,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.force_refund(payment_id, body.reason, body.refund_amount)
    return PaymentResponse.from_entity(payment)


@router.post("/payments/{payment_id}/void", response_model=PaymentResponse)
async def void_payment(
    payment_id: str,
    body: AdminVoidRequest,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.void_payment(payment_id, body.reason)
    return PaymentResponse.from_entity(payment)


@router.get("/transactions")
async def list_transactions(
    query: AdminPaginationQuery = Depends(),
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> list[dict]:
    return await use_case.list_transactions(query.to_criteria())


@router.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_transaction(transaction_id)


@router.post("/transactions/{transaction_id}/reverse")
async def reverse_transaction(
    transaction_id: str,
    body: ReverseTransactionRequest,
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.reverse_transaction(transaction_id, body.reason)


@router.get("/summary")
async def get_payments_summary(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_payments_summary()


@router.get("/summary/by-type")
async def get_summary_by_type(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_summary_by_type()


@router.get("/summary/by-method")
async def get_summary_by_payment_method(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_summary_by_payment_method()


@router.get("/summary/failed")
async def get_failed_payments_summary(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_failed_payments_summary()


@router.get("/summary/refunds")
async def get_refunds_summary(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_refunds_summary()


@router.get("/summary/transactions")
async def get_transactions_summary(
    _: Any = Depends(require_admin_user),
    use_case: AdminPaymentUseCases = Depends(get_admin_payment_use_cases),
) -> dict:
    return await use_case.get_transactions_summary()
