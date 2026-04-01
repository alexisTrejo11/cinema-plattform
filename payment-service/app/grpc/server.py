"""gRPC server entrypoint for the app-grpc Docker service.

Register servicers here when payment RPC implementations are wired to the
generated stubs under ``app.payments.infrastructure.grpc.generated``.
"""
from __future__ import annotations

import asyncio
import logging

import grpc

from app.config.app_config import settings

logger = logging.getLogger(__name__)


async def _serve() -> None:
    server = grpc.aio.server()
    addr = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(addr)
    logger.info("gRPC listening on %s (no servicers registered yet)", addr)
    await server.start()
    await server.wait_for_termination()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_serve())


if __name__ == "__main__":
    main()
