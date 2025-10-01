from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    provider: str
    auth_code: str | None = None


class ConnectionOut(BaseModel):
    id: int
    provider: str
    status: str

    class Config:
        from_attributes = True
