from __future__ import annotations
from typing import Dict, Any, List
from time import sleep, time
from app.agent.guardrails import redact_params, requires_confirmation, enforce_budgets
from app.observability.logging import logger
from app.config import settings
from app.capabilities.registry import get_capability


def execute_plan(org_id: int, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    start = time()
    tool_calls = 0
    cost_usd = 0.0

    for step in plan:
        if not enforce_budgets(tool_calls, time() - start, cost_usd, settings.agent_max_tool_calls, settings.agent_max_seconds, settings.agent_max_cost_usd):
            results.append({"status": "stopped", "reason": "budget_exceeded"})
            break

        capability_name = step["capability"]
        params = step.get("params", {})
        redacted = redact_params(params)

        if requires_confirmation(capability_name, params):
            results.append({"capability": capability_name, "status": "pending_confirmation", "params": redacted})
            continue

        try:
            cls = get_capability(capability_name)
            if not cls:
                results.append({"capability": capability_name, "status": "error", "error": f"Unknown capability {capability_name}"})
                continue
            instance = cls()  # type: ignore[call-arg]
            res = instance.execute(org_id, params)
            tool_calls += 1
            results.append({"capability": capability_name, "status": "success", "result": res})
        except Exception as e:
            results.append({"capability": capability_name, "status": "error", "error": str(e)})
            logger.exception("Capability execution failed")
            sleep(0.5)

    return results
