"""
Blocking gRPC server for this process (``cinema.ticket.v1.TicketService`` Ping).

Run: ``python -m app.grpc.server`` (see docker ``serve-grpc``).
Outbound calls to payment/billboard use clients in ``app.ticket.infrastructure.grpc``.
"""

from __future__ import annotations

import logging
from concurrent import futures

import grpc

import app.grpc  # noqa: F401 — bootstrap generated import path
from app.config.app_config import settings
from ticket.v1 import ticket_pb2, ticket_pb2_grpc

logger = logging.getLogger(__name__)


class _TicketServicer(ticket_pb2_grpc.TicketServiceServicer):
    def Ping(self, request, context):  # noqa: ARG002
        return ticket_pb2.PingResponse(
            service=settings.SERVICE_NAME,
            version=settings.API_VERSION,
        )


def run_grpc_server() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    ticket_pb2_grpc.add_TicketServiceServicer_to_server(_TicketServicer(), server)
    listen = f"[::]:{settings.GRPC_PORT}"
    server.add_insecure_port(listen)
    server.start()
    logger.info("gRPC server listening on %s (TicketService.Ping)", listen)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_grpc_server()
