from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel, HttpUrl
from app.capabilities.interface import Capability
from app.integrations.webhook import WebhookClient


class PostWebhookInput(BaseModel):
    url: HttpUrl
    payload: Dict[str, Any]


class PostWebhookOutput(BaseModel):
    ok: bool = True
    status: int


class PostWebhook(Capability):
    name = "post_webhook"
    Input = PostWebhookInput
    Output = PostWebhookOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = WebhookClient().post(str(data.url), data.payload)
        return PostWebhookOutput(ok=True, status=res.get("status", 200)).model_dump()
