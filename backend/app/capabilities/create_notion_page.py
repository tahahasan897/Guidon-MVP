from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.notion import NotionClient


class CreateNotionPageInput(BaseModel):
    title: str
    content: str


class CreateNotionPageOutput(BaseModel):
    ok: bool = True
    url: str | None = None


class CreateNotionPage(Capability):
    name = "create_notion_page"
    Input = CreateNotionPageInput
    Output = CreateNotionPageOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = NotionClient().create_page(data.title, data.content)
        return CreateNotionPageOutput(ok=True, url=res.get("url")).model_dump()
