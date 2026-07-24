import uuid
from datetime import datetime
from pydantic import BaseModel


class TagCreateModel(BaseModel):
    name: str


class TagResponse(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime
