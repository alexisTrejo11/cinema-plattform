#!/bin/bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "Building and starting billboard stack (Postgres, Redis, app.eplicas, NGINX)..."
docker-compose -f docker/docker-compose.yml up -d --build

echo
echo "Current services status:"
docker-compose -f docker/docker-compose.yml ps

echo
echo "Tailing NGINX logs (Ctrl+C to stop)..."
docker-compose -f docker/docker-compose.yml logs -f nginx

