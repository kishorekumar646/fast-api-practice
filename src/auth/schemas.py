from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=5)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    uid: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
