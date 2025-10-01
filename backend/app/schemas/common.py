from pydantic import BaseModel
from datetime import datetime


class Timestamped(BaseModel):
    created_at: datetime | None = None
