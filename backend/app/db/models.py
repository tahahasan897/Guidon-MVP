from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, JSON, DateTime, Boolean, Text, Float


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    org_id: Mapped[int | None] = mapped_column(ForeignKey("orgs.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Org(Base):
    __tablename__ = "orgs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Connection(Base):
    __tablename__ = "connections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    provider: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="connected")
    access_token_encrypted: Mapped[str] = mapped_column(Text)
    refresh_token_encrypted: Mapped[str | None]
    expires_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    kind: Mapped[str] = mapped_column(String(50))  # doc, slide, sheet, page
    provider: Mapped[str] = mapped_column(String(50))
    external_id: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EventIngested(Base):
    __tablename__ = "events_ingested"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    source: Mapped[str] = mapped_column(String(50))
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MetricDaily(Base):
    __tablename__ = "metrics_daily"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    mrr: Mapped[float] = mapped_column(Float, default=0.0)
    burn: Mapped[float] = mapped_column(Float, default=0.0)
    runway_months: Mapped[float] = mapped_column(Float, default=0.0)
    mom_growth: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AgentRun(Base):
    __tablename__ = "agent_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    mode: Mapped[str] = mapped_column(String(20))  # proactive|on_demand
    goal: Mapped[str | None]
    status: Mapped[str] = mapped_column(String(20), default="running")
    error: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AgentAction(Base):
    __tablename__ = "agent_actions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("agent_runs.id"))
    capability: Mapped[str] = mapped_column(String(100))
    params: Mapped[dict] = mapped_column(JSON)
    provider: Mapped[str | None]
    idempotency_key: Mapped[str] = mapped_column(String(255))
    requires_confirmation: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    output_summary: Mapped[str | None]
    error: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Preference(Base):
    __tablename__ = "preferences"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"))
    key: Mapped[str] = mapped_column(String(100))
    value: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
