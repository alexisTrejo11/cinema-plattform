#!/bin/sh

set -eu

if [ ! -f /etc/nginx/ssl/cert.pem ] || [ ! -f /etc/nginx/ssl/key.pem ]; then
    echo "Generating self-signed SSL certificates for development..."
    openssl req -x509 -newkey rsa:4096 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=CinemaPlatform/CN=localhost"
fi

exec "$@"