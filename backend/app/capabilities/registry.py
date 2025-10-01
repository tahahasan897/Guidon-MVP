from __future__ import annotations
from typing import Dict, Type
from app.capabilities.interface import Capability
from app.capabilities.create_document import CreateDocument
from app.capabilities.create_slide_deck import CreateSlideDeck
from app.capabilities.append_rows import AppendRows
from app.capabilities.update_cells import UpdateCells
from app.capabilities.post_message import PostMessage
from app.capabilities.post_webhook import PostWebhook
from app.capabilities.create_notion_page import CreateNotionPage


REGISTRY: Dict[str, Type[Capability]] = {
    CreateDocument.name: CreateDocument,
    CreateSlideDeck.name: CreateSlideDeck,
    AppendRows.name: AppendRows,
    UpdateCells.name: UpdateCells,
    PostMessage.name: PostMessage,
    PostWebhook.name: PostWebhook,
    CreateNotionPage.name: CreateNotionPage,
}


def get_capability(name: str) -> Type[Capability] | None:
    return REGISTRY.get(name)
