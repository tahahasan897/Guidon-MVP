SHELL := /bin/bash

.PHONY: up down logs migrate seed dev test fmt lint

up:
	docker compose -f infra/docker-compose.yml up -d --build

down:
	docker compose -f infra/docker-compose.yml down -v

logs:
	docker compose -f infra/docker-compose.yml logs -f | cat

migrate:
	docker compose -f infra/docker-compose.yml exec -w /app api bash -lc 'export PYTHONPATH=/app; alembic upgrade head'

seed:
	docker compose -f infra/docker-compose.yml exec api python -m app.seed || true

dev:
	UVICORN_RELOAD=true docker compose -f infra/docker-compose.yml up api worker web redis db

test:
	docker compose -f infra/docker-compose.yml exec api pytest -q || true
	docker compose -f infra/docker-compose.yml exec web npm run test --silent || true

fmt:
	docker compose -f infra/docker-compose.yml exec api ruff check --fix . && black .

lint:
	docker compose -f infra/docker-compose.yml exec api ruff check . && mypy app || true
