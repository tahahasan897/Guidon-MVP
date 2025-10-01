from typing import Dict, Any, List

class HubSpotClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def list_recent_contacts(self) -> List[Dict[str, Any]]:
        return [{"id": "1", "email": "lead@example.com"}]
