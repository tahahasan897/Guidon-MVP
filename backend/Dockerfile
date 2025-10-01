FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY backend/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt || true

COPY backend /app

EXPOSE 8000
CMD ["bash", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
