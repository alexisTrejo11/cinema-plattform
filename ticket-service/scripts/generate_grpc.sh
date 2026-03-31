#!/usr/bin/env bash
# Regenerate Python stubs from protos (run from repo root: ticket-service/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p app/grpc/generated
python -m grpc_tools.protoc \
  -I app/grpc/protos \
  --python_out=app/grpc/generated \
  --grpc_python_out=app/grpc/generated \
  app/grpc/protos/payment/v1/payment.proto \
  app/grpc/protos/billboard/v1/billboard.proto \
  app/grpc/protos/ticket/v1/ticket.proto
echo "Generated gRPC stubs under app/grpc/generated/"
