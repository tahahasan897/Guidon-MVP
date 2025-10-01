# founder-copilot (MVP)

Production-ready MVP that ingests business data (Sheets/CRM/accounting), analyzes it, and executes actions (update sheets, create docs/slides, post Slack).

## Stack
- Frontend: Next.js 14 (App Router, TypeScript, Tailwind), Clerk/NextAuth
- Backend: FastAPI (Python 3.11), SQLAlchemy, Alembic, Pydantic, Redis, RQ, Uvicorn
- DB: Postgres + pgvector
- LLM: OpenAI via LiteLLM
- Integrations: Google (Sheets/Docs/Slides), Notion, HubSpot, QuickBooks, Slack, Generic Webhook
- Infra: Docker Compose (web, api, worker, redis, postgres), Makefile, GitHub Actions CI

## Quickstart (Docker)

1. Copy env file and fill values:

```bash
cp .env.example .env
```

2. Start services:

```bash
make up
```

3. Run DB migrations:

```bash
make migrate
```

4. Open the app:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

## Make targets
- `make up`: start stack
- `make down`: stop stack
- `make dev`: run api in reload mode locally
- `make migrate`: run Alembic migrations
- `make test`: run unit tests (backend + frontend)

## Services
- api: FastAPI app
- worker: RQ worker
- web: Next.js
- db: Postgres + pgvector
- redis: Redis for queues

## Development
See `.env.example` for required variables. Secrets should be stored via Docker secrets or env vars; never log secrets.

## CI
GitHub Actions runs lint and tests for backend and frontend on PRs.
