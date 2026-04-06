"""Minimal gRPC process: listens on GRPC_PORT until real APIs are registered."""

import os
import signal
import sys
from concurrent import futures

import grpc


def _port() -> int:
    return int(os.environ.get("GRPC_PORT", "50051"))


def main() -> None:
    port = _port()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    print(
        f"gRPC listening on 0.0.0.0:{port} (placeholder; add services when protos exist)",
        flush=True,
    )

    def _stop(*_: object) -> None:
        server.stop(5)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
