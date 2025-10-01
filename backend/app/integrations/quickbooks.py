from typing import Dict, Any

class QuickBooksClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def get_latest_revenue_summary(self) -> Dict[str, Any]:
        return {"mrr": 0.0, "last_updated": "now"}
