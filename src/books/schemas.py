import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from pydantic import BaseModel


class ReviewInBook(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: uuid.UUID | None


class TagInBook(BaseModel):
    uid: uuid.UUID
    name: str


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class BookDetailModel(Book):
    reviews: List[ReviewInBook] = []
    tags: List[TagInBook] = []
