import uuid
from datetime import datetime
from pydantic import BaseModel


class AccountUpdateModel(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str


class AccountResponse(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
