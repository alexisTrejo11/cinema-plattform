from typing import List

from fastapi import APIRouter, Depends, Query, status
from starlette.responses import Response

from app.payments.application.commands import CreateStoredPaymentMethodCommand
from app.payments.application.usecases.customer_usecases import CustomerPaymentUseCases
from app.payments.presentation.depencies import get_customer_payment_use_cases
from app.payments.presentation.dtos import (
    CancelPaymentRequest,
    ConcessionsPurchaseRequest,
    InitiatePaymentRequest,
    InitiatePaymentResponse,
    MerchandisePurchaseRequest,
    PaymentResponse,
    PaymentSummaryResponse,
    ReceiptResponse,
    RefundRequest,
    StoredPaymentMethodResponse,
    SubscriptionPurchaseRequest,
    TicketPurchaseRequest,
    WalletCreditPurchaseRequest,
)
from app.shared.auth import AuthUserContext, get_current_user

router = APIRouter(prefix="/api/v1/payments/customers", tags=["Customer - Payments"])


@router.get("/history", response_model=List[PaymentResponse])
async def get_my_payment_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> List[PaymentResponse]:
    payments = await use_case.get_payment_history(str(user.id), limit=limit, offset=offset)
    return [PaymentResponse.from_entity(payment) for payment in payments]


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_my_payment_detail(
    payment_id: str,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.get_payment_detail(str(user.id), payment_id)
    return PaymentResponse.from_entity(payment)


@router.get("/summary", response_model=PaymentSummaryResponse)
async def get_my_payment_summary(
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentSummaryResponse:
    summary = await use_case.get_payment_summary(str(user.id))
    return PaymentSummaryResponse(**summary)


@router.get("/payments/{payment_id}/receipt", response_model=ReceiptResponse)
async def get_receipt(
    payment_id: str,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> ReceiptResponse:
    receipt = await use_case.get_receipt(str(user.id), payment_id)
    return ReceiptResponse(**receipt)


@router.post("/initiate", response_model=InitiatePaymentResponse)
async def initiate_payment(
    body: InitiatePaymentRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> InitiatePaymentResponse:
    response = await use_case.initiate_payment(str(user.id), body.payment_id)
    return InitiatePaymentResponse(**response)


@router.post("/payments/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payment_id: str,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.confirm_payment(str(user.id), payment_id)
    return PaymentResponse.from_entity(payment)


@router.post("/payments/{payment_id}/cancel", response_model=PaymentResponse)
async def cancel_payment(
    payment_id: str,
    body: CancelPaymentRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.cancel_payment(str(user.id), payment_id, body.reason)
    return PaymentResponse.from_entity(payment)


@router.post("/payments/{payment_id}/refund", response_model=PaymentResponse)
async def request_refund(
    payment_id: str,
    body: RefundRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.request_refund(
        str(user.id), payment_id, reason=body.reason, refund_amount=body.refund_amount
    )
    return PaymentResponse.from_entity(payment)


@router.post("/tickets", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def purchase_tickets(
    body: TicketPurchaseRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.purchase_tickets(body.to_command(str(user.id)))
    return PaymentResponse.from_entity(payment)


@router.post(
    "/consessions",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def purchase_consessions(
    body: ConcessionsPurchaseRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.purchase_concessions(body.to_command(str(user.id)))
    return PaymentResponse.from_entity(payment)


@router.post(
    "/merchandise",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def purchase_merchandise(
    body: MerchandisePurchaseRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.purchase_merchandise(body.to_command(str(user.id)))
    return PaymentResponse.from_entity(payment)


@router.post(
    "/subscriptions",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def purchase_subscriptions(
    body: SubscriptionPurchaseRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.purchase_subscriptions(body.to_command(str(user.id)))
    return PaymentResponse.from_entity(payment)


@router.post(
    "/wallets/credit",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def purchase_wallet_credit(
    body: WalletCreditPurchaseRequest,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> PaymentResponse:
    payment = await use_case.purchase_wallet_credit(body.to_command(str(user.id)))
    return PaymentResponse.from_entity(payment)


@router.get("/payment-methods", response_model=List[StoredPaymentMethodResponse])
async def get_customer_stored_payment_methods(
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> List[StoredPaymentMethodResponse]:
    rows = await use_case.list_customer_stored_payment_methods(str(user.id))
    return [StoredPaymentMethodResponse(**row) for row in rows]


@router.post(
    "/payment-methods",
    response_model=StoredPaymentMethodResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_stored_payment_method(
    body: CreateStoredPaymentMethodCommand,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> StoredPaymentMethodResponse:
    command = body.model_copy(update={"user_id": str(user.id)})
    created = await use_case.create_customer_stored_payment_method(command)
    return StoredPaymentMethodResponse(**created)


@router.delete("/payment-methods/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_stored_payment_method(
    payment_method_id: str,
    user: AuthUserContext = Depends(get_current_user),
    use_case: CustomerPaymentUseCases = Depends(get_customer_payment_use_cases),
) -> Response:
    await use_case.delete_customer_stored_payment_method(str(user.id), payment_method_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
