from typing import Dict, Any

class SlackClient:
    def __init__(self, bot_token: str | None = None):
        self.bot_token = bot_token

    def post_message(self, channel: str, text: str) -> Dict[str, Any]:
        return {"channel": channel, "ts": "123.456", "ok": True, "text": text}
