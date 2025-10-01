from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.google_docs import GoogleDocsClient
from app.integrations.notion import NotionClient


class CreateDocumentInput(BaseModel):
    title: str
    content: str
    provider: str | None = None  # google_docs|notion


class CreateDocumentOutput(BaseModel):
    ok: bool = True
    url: str | None = None


class CreateDocument(Capability):
    name = "create_document"
    Input = CreateDocumentInput
    Output = CreateDocumentOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        if data.provider == "notion":
            res = NotionClient().create_page(data.title, data.content)
            return CreateDocumentOutput(ok=True, url=res.get("url")).model_dump()
        res = GoogleDocsClient().create_document(data.title, data.content)
        return CreateDocumentOutput(ok=True, url=res.get("url")).model_dump()
