from pydantic import BaseModel


class NodeResponse(BaseModel):
    id: str
    number: str
    title: str
    level: int
    content: str
    content_hash: str | None = None

    class Config:
        from_attributes = True