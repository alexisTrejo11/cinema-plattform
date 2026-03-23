import asyncio
import logging
import os

import grpc

from app.config.db.postgres_config import AsyncSessionLocal
from app.grpc.generated import concession_pb2_grpc
from app.grpc.services.concession_catalog_servicer import ConcessionCatalogGrpcServicer

logger = logging.getLogger(__name__)


async def serve_grpc(host: str = "0.0.0.0", port: int = 50051) -> None:
    server = grpc.aio.server()
    concession_pb2_grpc.add_ConcessionCatalogServiceServicer_to_server(
        ConcessionCatalogGrpcServicer(AsyncSessionLocal), server
    )
    bind_address = f"{host}:{port}"
    server.add_insecure_port(bind_address)

    await server.start()
    logger.info("Concession gRPC server started on %s", bind_address)
    await server.wait_for_termination()


if __name__ == "__main__":
    grpc_host = os.getenv("GRPC_HOST", "0.0.0.0")
    grpc_port = int(os.getenv("GRPC_PORT", "50051"))
    asyncio.run(serve_grpc(host=grpc_host, port=grpc_port))
