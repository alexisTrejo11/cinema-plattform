FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-openbsd \
    postgresql-client \  
    bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import redis; redis.Redis(host='redis', port=6379).ping()" || exit 1

ENTRYPOINT ["/app/init_db.sh"]

CMD ["uvicorn", "main:app", "--reload" ,"--host", "0.0.0.0", "--port", "8000"]