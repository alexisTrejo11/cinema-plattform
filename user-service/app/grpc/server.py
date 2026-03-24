import asyncio
import logging

from grpc import aio

from app.grpc.servicer import UsersGrpcServicer
from app.grpc.generated import users_pb2_grpc
from app.shared.logging import setup_logging
from config.app_config import settings

logger = logging.getLogger(__name__)


async def _serve() -> None:
    setup_logging()
    server = aio.server()
    users_pb2_grpc.add_UsersServiceServicer_to_server(UsersGrpcServicer(), server)
    listen = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(listen)
    await server.start()
    logger.info("gRPC UsersService listening on %s", listen)
    await server.wait_for_termination()


def main() -> None:
    asyncio.run(_serve())


if __name__ == "__main__":
    main()
