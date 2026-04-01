"""
HTTP API for the **payment method catalog** (checkout options: card, Oxxo, etc.).

These routes expose CRUD-style operations on catalog rows stored in
``payment_methods``. Saved customer cards live under a different API surface.

OpenAPI / ReDoc pick up ``summary``, ``description``, ``response_model``, and
``responses``; request/response models carry ``Field`` descriptions and
``json_schema_extra`` examples.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from starlette.responses import Response

from app.payments.application.commands import (
    CreatePaymentMethodCommand,
    UpdatePaymentMethodCommand,
)
from app.payments.application.usecases.payment_method_usecases import (
    PaymentMethodUseCases,
)
from app.payments.presentation.dtos import PaymentMethodResponse, UpdatePaymentMethodRequest
from app.shared.auth import AuthUserContext, require_admin_user
from app.shared.documentation import common_error_responses

from ..depencies import get_payment_method_use_cases

_NO_CONTENT = {
    status.HTTP_204_NO_CONTENT: {
        "description": "Success. No response body.",
    }
}

_ADMIN_ERRORS = {
    **common_error_responses,
}

_READ_LIST_ERRORS = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: common_error_responses[
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ],
    status.HTTP_503_SERVICE_UNAVAILABLE: common_error_responses[
        status.HTTP_503_SERVICE_UNAVAILABLE
    ],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_error_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}

_READ_ONE_ERRORS = {
    **_READ_LIST_ERRORS,
    status.HTTP_404_NOT_FOUND: common_error_responses[status.HTTP_404_NOT_FOUND],
}

router = APIRouter(
    prefix="/api/v2/payment/methods",
    tags=["Payment Methods"],
)


@router.get(
    "/",
    response_model=List[PaymentMethodResponse],
    status_code=status.HTTP_200_OK,
    summary="List catalog payment methods",
    description=(
        "Returns every **non-deleted** payment method configured for checkout. "
        "Public read; does not include per-user saved cards."
    ),
    responses=_READ_LIST_ERRORS,
)
async def list_payment_methods(
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> List[PaymentMethodResponse]:
    """Load all active catalog rows (``deleted_at IS NULL``)."""
    payment_methods = await use_case.get_all_payment_methods()
    return [PaymentMethodResponse.from_entity(pm) for pm in payment_methods]


@router.get(
    "/{payment_method_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Get one payment method",
    description=(
        "Fetches a single catalog entry by id. "
        "Returns **404** if the id is unknown or the row is soft-deleted "
        "(use restore + admin flows to see deleted rows)."
    ),
    responses=_READ_ONE_ERRORS,
)
async def get_payment_method(
    payment_method_id: str,
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> PaymentMethodResponse:
    """Resolve ``payment_method_id`` to a catalog ``PaymentMethod``."""
    payment_method = await use_case.get_payment_method(payment_method_id)
    return PaymentMethodResponse.from_entity(payment_method)


@router.post(
    "/",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create payment method",
    description=(
        "Registers a new checkout option. **Admin only.** "
        "The server assigns a new UUID as ``id``."
    ),
    responses=_ADMIN_ERRORS,
)
async def create_payment_method(
    request_data: CreatePaymentMethodCommand,
    _: AuthUserContext = Depends(require_admin_user),
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> PaymentMethodResponse:
    """Persist a new catalog row from the command body."""
    payment_method = await use_case.create_payment_method(request_data)
    return PaymentMethodResponse.from_entity(payment_method)


@router.put(
    "/{payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Update payment method",
    description=(
        "Partial update of a catalog row. **Admin only.** "
        "Omitted JSON fields are left unchanged. "
        "The id in the URL is always used; any ``id`` in an old client body is ignored."
    ),
    responses={**_NO_CONTENT, **_ADMIN_ERRORS},
)
async def update_payment_method(
    payment_method_id: str,
    body: UpdatePaymentMethodRequest,
    _: AuthUserContext = Depends(require_admin_user),
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> Response:
    """Merge ``body`` into the existing row identified by ``payment_method_id``."""
    command = UpdatePaymentMethodCommand(
        id=payment_method_id,
        **body.model_dump(exclude_unset=True),
    )
    await use_case.update_payment_method(command)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{payment_method_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Restore soft-deleted payment method",
    description=(
        "Clears ``deleted_at`` and reactivates the catalog row. **Admin only.**"
    ),
    responses={**_NO_CONTENT, **_ADMIN_ERRORS},
)
async def restore_payment_method(
    payment_method_id: str,
    _: AuthUserContext = Depends(require_admin_user),
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> Response:
    """Undo soft-delete for ``payment_method_id`` if it exists."""
    await use_case.restore_payment_method(payment_method_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Soft-delete payment method",
    description=(
        "Marks the catalog row as deleted (sets ``deleted_at``). **Admin only.** "
        "Does not remove the row from the database."
    ),
    responses={**_NO_CONTENT, **_ADMIN_ERRORS},
)
async def delete_payment_method(
    payment_method_id: str,
    _: AuthUserContext = Depends(require_admin_user),
    use_case: PaymentMethodUseCases = Depends(get_payment_method_use_cases),
) -> Response:
    """Soft-delete by default (hard delete is handled inside the use case if extended)."""
    await use_case.delete_payment_method(payment_method_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
