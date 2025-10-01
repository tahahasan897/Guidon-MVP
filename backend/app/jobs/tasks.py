from time import sleep
from sqlalchemy.orm import Session
from app.observability.logging import logger
from app.agent.planner import plan_for_goal
from app.agent.executor import execute_plan
from app.db.session import SessionLocal
from app.db import models


def run_agent_job(org_id: int, goal: str | None, mode: str = "on_demand") -> dict:
    logger.info(f"Starting agent job org_id={org_id} goal={goal} mode={mode}")
    state = {"metrics": {}}
    plan = plan_for_goal(org_id, goal, state)
    results = execute_plan(org_id, plan)
    return {"status": "completed", "results": results}


def execute_action_job(action_id: int) -> dict:
    logger.info(f"Executing action action_id={action_id}")
    db: Session = SessionLocal()
    try:
        action = db.query(models.AgentAction).get(action_id)
        if not action:
            return {"status": "error", "error": "Action not found"}
        # Execute a single-step plan for this action
        results = execute_plan(1, [{"capability": action.capability, "params": action.params}])
        r = results[0] if results else {"status": "error", "error": "No result"}
        if r.get("status") == "success":
            action.status = "success"
            action.output_summary = str(r.get("result"))[:512]
        elif r.get("status") == "pending_confirmation":
            action.status = "pending"
            action.requires_confirmation = True
        else:
            action.status = "error"
            action.error = str(r.get("error"))[:512]
        db.commit()
        return {"status": action.status}
    finally:
        db.close()
