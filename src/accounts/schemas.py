import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class Account(BaseModel):
    uid: uuid.UUID
    username: str
    password: str
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime

class AccountCreateModel(BaseModel):
    username: str
    password: str
    email: str
    full_name: str

class AccountUpdateModel(BaseModel):
    username: str
    password: str
    email: str
    full_name: str

class LoginModel(BaseModel):
    username: str
    password: str

