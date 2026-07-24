import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreateModel(BaseModel):
    rating: int = Field(gt=0, lt=5)
    review_text: str


class ReviewUpdateModel(BaseModel):
    rating: int = Field(gt=0, lt=5)
    review_text: str


class ReviewResponse(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: uuid.UUID | None
    book_uid: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
