from typing import Dict, Any

class WebhookClient:
    def post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"url": url, "status": 200, "payload_size": len(str(payload))}
