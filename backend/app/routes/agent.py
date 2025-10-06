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

class MarketingCampaignRequest(BaseModel):
    org_id: int
    campaign_type: str = "lead_gen"  # lead_gen, awareness, conversion
    target_audience: str
    budget_usd: float = 100.0
    duration_days: int = 30
    goal: str | None = None

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

@router.post("/marketing-campaign")
def run_marketing_campaign(payload: MarketingCampaignRequest, org_id: int = Header(..., alias="X-Org-Id"), db: Session = Depends(get_db)):
    """
    Launch a sophisticated marketing campaign for SMBs/startups.
    
    Campaign types:
    - lead_gen: Focus on generating qualified leads
    - awareness: Build brand awareness and thought leadership  
    - conversion: Optimize for sales conversions
    
    Example request:
    {
        "campaign_type": "lead_gen",
        "target_audience": "SaaS startups in fintech",
        "budget_usd": 500.0,
        "duration_days": 30,
        "goal": "Generate 100 qualified leads"
    }
    """
    # Create DB row
    run = models.AgentRun(
        org_id=org_id, 
        mode="marketing_campaign", 
        goal=payload.goal or f"{payload.campaign_type} campaign for {payload.target_audience}",
        status="running"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    
    # Enqueue the sophisticated marketing campaign job
    job = enqueue(
        "app.jobs.marketing_campaign.marketing_campaign_job",
        run_id=run.id,
        campaign_type=payload.campaign_type,
        target_audience=payload.target_audience,
        budget_usd=payload.budget_usd,
        duration_days=payload.duration_days
    )
    
    return {
        "run_id": run.id, 
        "status": "queued",
        "campaign_type": payload.campaign_type,
        "target_audience": payload.target_audience,
        "budget_usd": payload.budget_usd,
        "duration_days": payload.duration_days,
        "estimated_completion": "2-3 minutes"
    }

class ConfirmRequest(BaseModel):
    action_id: int

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