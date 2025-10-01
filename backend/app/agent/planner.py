from __future__ import annotations
from typing import List, Dict, Any


def plan_for_goal(org_id: int, goal: str | None, state: Dict[str, Any]) -> List[Dict[str, Any]]:
    actions: List[Dict[str, Any]] = []
    goal_text = (goal or "").lower()

    if "investor" in goal_text or "weekly" in goal_text or "summary" in goal_text:
        actions.append({
            "capability": "create_document",
            "params": {"title": "Weekly Growth Summary", "content": "Auto-generated summary of growth metrics."},
            "rationale": "Prepare an investor-friendly document summarizing growth.",
            "confirm_required": False,
        })
        actions.append({
            "capability": "post_message",
            "params": {"channel": "#exec-updates", "text": "Weekly growth summary created. See Docs for details."},
            "rationale": "Notify stakeholders in Slack.",
            "confirm_required": False,
        })
    else:
        actions.append({
            "capability": "post_message",
            "params": {"channel": "#ops", "text": f"Ran on-demand goal: {goal or 'none'}"},
            "rationale": "Acknowledge run and record status",
            "confirm_required": False,
        })

    return actions
