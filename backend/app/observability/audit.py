from __future__ import annotations
from typing import Any, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import models
from app.agent.guardrails import redact_params


def log_action(
    db: Session,
    run_id: int,
    capability: str,
    params: Dict[str, Any],
    provider: str | None,
    idempotency_key: str,
    requires_confirmation: bool,
    status: str,
    output_summary: str | None = None,
    error: str | None = None,
) -> models.AgentAction:
    action = models.AgentAction(
        run_id=run_id,
        capability=capability,
        params=redact_params(params),
        provider=provider,
        idempotency_key=idempotency_key,
        requires_confirmation=requires_confirmation,
        status=status,
        output_summary=output_summary,
        error=error,
        created_at=datetime.utcnow(),
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action
