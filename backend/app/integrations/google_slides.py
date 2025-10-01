from typing import Dict, Any

class GoogleSlidesClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def create_slide_deck(self, title: str) -> Dict[str, Any]:
        return {"deck_id": "deck_123", "title": title, "url": "https://slides.google.com/presentation/d/deck_123"}
