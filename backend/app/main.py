from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.observability.logging import setup_logging, logger
from app.routes import connections, metrics, agent, runs, actions
from app.ingest import webhooks as ingest_webhooks
from app.db.models import Base
from app.db.session import engine

setup_logging(settings.log_level)

app = FastAPI(title="founder-copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}


app.include_router(connections.router)
app.include_router(metrics.router)
app.include_router(agent.router)
app.include_router(runs.router)
app.include_router(actions.router)
app.include_router(ingest_webhooks.router)
