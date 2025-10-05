from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4

from app.jobs.queue import enqueue
from app.db.session import get_db
from app.db import models
from app.agent.planner import plan_for_goal
from app.agent.guardrails import requires_confirmation
from app.observability.audit import log_action

router = APIRouter(prefix="/api/agent", tags=["agent"])

class RunRequest(BaseModel):
    org_id: int
    goal: str | None = None
    mode: str = "on_demand"


@router.post("/run")
def run_agent(req: RunRequest, db: Session = Depends(get_db)):
    run = models.AgentRun(org_id=req.org_id, mode=req.mode, goal=req.goal, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    plan = plan_for_goal(req.org_id, req.goal, state={})

    for step in plan:
        capability = step["capability"]
        params = step.get("params", {})
        needs_confirm = step.get("confirm_required", False) or requires_confirmation(capability, params)
        idempotency_key = str(uuid4())
        action = log_action(
            db=db,
            run_id=run.id,
            capability=capability,
            params=params,
            provider=None,
            idempotency_key=idempotency_key,
            requires_confirmation=needs_confirm,
            status="pending" if needs_confirm else "queued",
        )
        if not needs_confirm:
            enqueue("app.jobs.tasks.execute_action_job", action.id)

    run.status = "queued"
    db.commit()
    return {"run_id": run.id, "status": run.status, "goal": run.goal, "mode": run.mode}


class ConfirmRequest(BaseModel):
    action_id: int

@router.post("/run-hello")
def run_hello_job(payload: RunRequest, org_id: int = Header(..., alias="X-Org-Id"), db: Session = Depends(get_db)):
    # Create DB row
    run = models.AgentRun(org_id=org_id, mode=payload.mode, goal=payload.goal, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    
    job = enqueue("app.jobs.hello.hello_world", run_id=run.id, name=payload.goal or "friend")
    return {"run_id": run.id, "status": "queued"}

@router.post("/confirm_action")
def confirm_action(req: ConfirmRequest, db: Session = Depends(get_db)):
    action = db.query(models.AgentAction).get(req.action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if not action.requires_confirmation:
        return {"action_id": action.id, "status": action.status}
    action.requires_confirmation = False
    action.status = "queued"
    db.commit()
    enqueue("app.jobs.tasks.execute_action_job", action.id)
    return {"action_id": action.id, "status": action.status}
