from hashlib import md5
from typing import Dict, Any, List
from app.integrations.google_sheets import GoogleSheetsClient
from app.integrations.quickbooks import QuickBooksClient


class SheetsPoller:
    def __init__(self, token: str | None = None):
        self.client = GoogleSheetsClient(token)

    def hash_range(self, values: List[List[Any]]) -> str:
        flat = "".join(["|".join(map(str, r)) for r in values])
        return md5(flat.encode()).hexdigest()

    def check_changes(self, spreadsheet_id: str, range_a1: str) -> Dict[str, Any]:
        # Stub: no real fetch; pretend values changed
        values = [["A", 1], ["B", 2]]
        return {"hash": self.hash_range(values), "changed": True}


class QuickBooksPoller:
    def __init__(self, token: str | None = None):
        self.client = QuickBooksClient(token)

    def get_revenue_snapshot(self) -> Dict[str, Any]:
        return self.client.get_latest_revenue_summary()
