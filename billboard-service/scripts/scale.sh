#!/bin/bash

set -euo pipefail

INSTANCES=${1:-3}

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "Scaling app.eplicas to ${INSTANCES}..."
docker-compose -f docker/docker-compose.yml up -d --scale app.=${INSTANCES}

