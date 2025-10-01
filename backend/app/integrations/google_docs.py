from typing import Dict, Any

class GoogleDocsClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def create_document(self, title: str, content: str) -> Dict[str, Any]:
        return {"doc_id": "doc_123", "title": title, "url": "https://docs.google.com/document/d/doc_123"}
