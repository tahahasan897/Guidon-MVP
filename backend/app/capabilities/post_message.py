from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.slack import SlackClient


class PostMessageInput(BaseModel):
    channel: str
    text: str


class PostMessageOutput(BaseModel):
    ok: bool = True
    ts: str | None = None


class PostMessage(Capability):
    name = "post_message"
    Input = PostMessageInput
    Output = PostMessageOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = SlackClient().post_message(data.channel, data.text)
        return PostMessageOutput(ok=True, ts=res.get("ts")).model_dump()
