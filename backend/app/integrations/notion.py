from typing import Dict, Any

class NotionClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def create_page(self, title: str, content: str) -> Dict[str, Any]:
        return {"page_id": "page_123", "title": title, "url": "https://www.notion.so/page_123"}
