from __future__ import annotations
from typing import Any, Dict, Protocol
from pydantic import BaseModel


class CapabilityInput(BaseModel):
    pass


class CapabilityOutput(BaseModel):
    ok: bool = True
    summary: str | None = None


class Capability(Protocol):
    name: str
    Input: type[BaseModel]
    Output: type[BaseModel]

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        ...
