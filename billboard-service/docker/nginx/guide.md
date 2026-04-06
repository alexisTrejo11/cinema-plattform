# Docker + NGINX Load Balancing & SSL Implementation Guide

## Current Environment Setup
```
Project: billboard-service (FastAPI with PostgreSQL, Redis)
Current: Single Docker container for API
Target: Multi-instance FastAPI with NGINX load balancer + SSL
```

## Step-by-Step Implementation Tasks

### **Phase 1: Prepare FastAPI for Multiple Instances**

```bash
# 1. Install required dependencies
pip install gunicorn
```

**Task 1.1:** Update your existing Dockerfile
```dockerfile
# Replace the last line (CMD) with:
CMD ["gunicorn", "main:fast_api_app. "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### **Phase 2: Create NGINX Configuration**

**Task 2.1:** Create nginx directory structure
```bash
mkdir -p nginx/ssl
```

**Task 2.2:** Create `nginx/nginx.conf`
```nginx
events {
    worker_connections 1024;
}

http {
    upstream billboard_servers {
        server billboard-app.:8000;
        server billboard-app.:8000;
        server billboard-app.:8000;
    }

    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

    server {
        listen 80;
        server_name localhost;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_cache api_cache;
            proxy_cache_valid 200 5m;
            
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_pass http://billboard_servers;
        }

        location /health {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
```

**Task 2.3:** Create `nginx/Dockerfile`
```dockerfile
FROM nginx:alpine
RUN apk add --no-cache openssl
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/ssl
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

**Task 2.4:** Create `nginx/entrypoint.sh`
```bash
#!/bin/sh
if [ ! -f /etc/nginx/ssl/cert.pem ] || [ ! -f /etc/nginx/ssl/key.pem ]; then
    echo "Generating SSL certificates for development..."
    openssl req -x509 -newkey rsa:4096 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
fi
exec "$@"
```

### **Phase 3: Update Docker Compose**

**Task 3.1:** Create/Update `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-billboard}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-billboard123}
      POSTGRES_DB: ${DB_NAME:-billboard}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - billboard_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U billboard"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    networks:
      - billboard_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  billboard-app.:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER:-billboard}:${DB_PASSWORD:-billboard123}@postgres:5432/${DB_NAME:-billboard}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - billboard_network
    volumes:
      - ./logs:/app.ogs

  billboard-app.:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER:-billboard}:${DB_PASSWORD:-billboard123}@postgres:5432/${DB_NAME:-billboard}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - billboard_network
    volumes:
      - ./logs:/app.ogs

  billboard-app.:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER:-billboard}:${DB_PASSWORD:-billboard123}@postgres:5432/${DB_NAME:-billboard}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - billboard_network
    volumes:
      - ./logs:/app.ogs

  nginx:
    build: ./nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - billboard-app.
      - billboard-app.
      - billboard-app.
    networks:
      - billboard_network
    volumes:
      - ./nginx/logs:/var/log/nginx

networks:
  billboard_network:
    driver: bridge

volumes:
  postgres_data:
```

**Task 3.2:** Create `.env` file
```env
DB_USER=billboard
DB_PASSWORD=billboard123
DB_NAME=billboard
app.AME=Billboard Service
app.ERSION=1.0.0
REDIS_URL=redis://redis:6379
```

### **Phase 4: Update Requirements**

**Task 4.1:** Add to `requirements.txt`
```txt
gunicorn>=20.1.0
```

### **Phase 5: Create Utility Scripts**

**Task 5.1:** Create `scripts/deploy.sh`
```bash
#!/bin/bash
echo "Building and starting services..."
docker-compose up -d --build
echo "Services status:"
docker-compose ps
echo "Logs:"
docker-compose logs -f nginx
```

**Task 5.2:** Create `scripts/scale.sh`
```bash
#!/bin/bash
INSTANCES=${1:-3}
echo "Scaling to $INSTANCES instances..."
docker-compose up -d --scale billboard-app.INSTANCES
```

**Task 5.3:** Make scripts executable
```bash
chmod +x scripts/*.sh
```

### **Phase 6: Testing**

**Task 6.1:** Test the setup
```bash
# 1. Stop any running containers
docker-compose down

# 2. Build and start
docker-compose up -d --build

# 3. Check logs
docker-compose logs -f nginx

# 4. Test endpoints (in another terminal)
curl -k https://localhost/api/movies
curl -k https://localhost/api/movies  # Should hit different instance

# 5. Check load balancing
docker-compose logs billboard-app. | grep "GET"
docker-compose logs billboard-app. | grep "GET"
docker-compose logs billboard-app. | grep "GET"
```

### **Phase 7: Production SSL (Optional - for real domain)**

**Task 7.1:** Create `nginx/nginx.prod.conf` (for real domain)
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of configuration same as nginx.conf
}
```

**Task 7.2:** Add certbot to docker-compose for production
```yaml
# Add to docker-compose.yml
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/www:/var/www/certbot
    - ./certbot/conf:/etc/letsencrypt
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

## Execution Order

```bash
# Execute in this sequence:
1. cd /path/to/billboard-service
2. mkdir -p nginx/ssl scripts
3. # Create all files mentioned above
4. pip install gunicorn
5. chmod +x scripts/*.sh
6. ./scripts/deploy.sh
7. # Test the endpoints
8. # If production: update domain and use nginx.prod.conf
```

## Verification Checklist

- [ ] All 3 FastAPI instances are running (`docker-compose ps`)
- [ ] NGINX is running and exposes ports 80/443
- [ ] HTTPS works with self-signed certificate
- [ ] Load balancing distributes requests evenly
- [ ] PostgreSQL and Redis are accessible from all instances
- [ ] Health check endpoint returns 200
- [ ] Cache is working across instances (shared Redis)

## Troubleshooting Commands

```bash
# Check logs
docker-compose logs nginx
docker-compose logs billboard-app.

# Enter containers
docker-compose exec nginx sh
docker-compose exec billboard-app. bash

# Test internal communication
docker-compose exec nginx curl http://billboard-app.:8000/health

# Restart specific service
docker-compose restart nginx

# Scale down/up
docker-compose up -d --scale billboard-app.
```

This setup gives you:
- ✅ Load balancing across 3 FastAPI instances
- ✅ SSL termination at NGINX
- ✅ Shared Redis cache
- ✅ Single PostgreSQL database
- ✅ Easy scaling (just change the scale parameter)
- ✅ Development SSL certificates auto-generated