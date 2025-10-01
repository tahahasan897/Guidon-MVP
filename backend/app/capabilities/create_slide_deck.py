from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.google_slides import GoogleSlidesClient


class CreateSlideDeckInput(BaseModel):
    title: str


class CreateSlideDeckOutput(BaseModel):
    ok: bool = True
    url: str | None = None


class CreateSlideDeck(Capability):
    name = "create_slide_deck"
    Input = CreateSlideDeckInput
    Output = CreateSlideDeckOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = GoogleSlidesClient().create_slide_deck(data.title)
        return CreateSlideDeckOutput(ok=True, url=res.get("url")).model_dump()
