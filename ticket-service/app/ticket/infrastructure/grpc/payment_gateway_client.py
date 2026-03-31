"""
Outbound adapter: payment / wallet service over gRPC.

Implements :class:`~app.ticket.domain.ports.PaymentGatewayPort`.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

import grpc

import app.grpc  # noqa: F401 — bootstrap generated import path
from app.config.app_config import settings
from app.ticket.domain.exceptions import PaymentAuthorizationFailedError
from app.ticket.domain.ports import (
    PaymentAuthorizationRequest,
    PaymentAuthorizationResult,
    PaymentGatewayPort,
    PaymentRefundRequest,
    PaymentRefundResult,
)
from payment.v1 import payment_pb2, payment_pb2_grpc

_log = logging.getLogger(__name__)

_client: Optional["GrpcPaymentGatewayClient"] = None


class GrpcPaymentGatewayClient(PaymentGatewayPort):
    """gRPC client for ``cinema.payment.v1.PaymentService`` (authorize + refund)."""

    def __init__(self, target: str, timeout: float) -> None:
        self._channel = grpc.insecure_channel(target)
        self._stub = payment_pb2_grpc.PaymentServiceStub(self._channel)
        self._timeout = timeout

    async def authorize_payment(
        self, request: PaymentAuthorizationRequest
    ) -> PaymentAuthorizationResult:
        proto = payment_pb2.AuthorizePaymentRequest(
            amount=str(request.amount),
            currency=request.currency,
            customer_id=request.customer_id,
            idempotency_key=request.idempotency_key,
            payment_method=request.payment_method,
            payment_token=request.payment_token,
            customer_ip=request.customer_ip or "",
        )
        loop = asyncio.get_running_loop()
        try:
            resp = await loop.run_in_executor(
                None,
                lambda: self._stub.AuthorizePayment(proto, timeout=self._timeout),
            )
        except grpc.RpcError as exc:
            _log.warning("payment AuthorizePayment failed: %s", exc)
            raise PaymentAuthorizationFailedError(
                f"gRPC {exc.code().name}: {exc.details() or 'payment service error'}"
            ) from exc

        return PaymentAuthorizationResult(
            authorized=resp.authorized,
            transaction_id=resp.transaction_id or "",
        )

    async def refund_payment(self, request: PaymentRefundRequest) -> PaymentRefundResult:
        proto = payment_pb2.RefundPaymentRequest(
            ticket_id=request.ticket_id,
            transaction_id=request.transaction_id,
            amount=str(request.amount),
            currency=request.currency,
            reason=request.reason or "",
        )
        loop = asyncio.get_running_loop()
        try:
            resp = await loop.run_in_executor(
                None,
                lambda: self._stub.RefundPayment(proto, timeout=self._timeout),
            )
        except grpc.RpcError as exc:
            _log.warning("payment RefundPayment failed: %s", exc)
            raise RuntimeError(
                f"gRPC refund failed {exc.code().name}: {exc.details()}"
            ) from exc

        return PaymentRefundResult(refund_id=resp.refund_id or "", status=resp.status or "")


def get_shared_payment_gateway_client() -> Optional[GrpcPaymentGatewayClient]:
    """Singleton client when ``GRPC_PAYMENT_TARGET`` is set; otherwise ``None``."""
    global _client
    target = settings.GRPC_PAYMENT_TARGET.strip()
    if not target:
        return None
    if _client is None:
        _client = GrpcPaymentGatewayClient(target, settings.GRPC_TIMEOUT_SECONDS)
        _log.info("gRPC payment client target=%s", target)
    return _client
