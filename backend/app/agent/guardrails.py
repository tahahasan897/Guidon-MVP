from __future__ import annotations
from typing import Dict, Any

SENSITIVE_CAPABILITIES = {"send_email", "delete_data"}


def redact_params(params: Dict[str, Any]) -> Dict[str, Any]:
    redacted = {}
    for k, v in params.items():
        if any(token in k.lower() for token in ["token", "secret", "password"]):
            redacted[k] = "[REDACTED]"
        else:
            redacted[k] = v
    return redacted


def requires_confirmation(capability: str, params: Dict[str, Any]) -> bool:
    if capability in SENSITIVE_CAPABILITIES:
        return True
    # heuristic: emails or external send
    txt = str(params).lower()
    if "email" in txt or "send" in txt:
        return True
    return False


def enforce_budgets(step_count: int, elapsed_s: float, cost_usd: float, max_steps: int, max_seconds: int, max_cost: float) -> bool:
    if step_count >= max_steps:
        return False
    if elapsed_s >= max_seconds:
        return False
    if cost_usd >= max_cost:
        return False
    return True
