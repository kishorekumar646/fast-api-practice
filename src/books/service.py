import uuid
from datetime import datetime
from typing import List, Any

from sqlalchemy import Row
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.errors import BookAlreadyExists
from .interfaces import IBookService
from .schemas import BookCreateModel, BookUpdateModel


class BookService(IBookService):

    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        result = await session.exec(select(Book))
        return list(result.all())

    async def get_user_books(self, user_uid: uuid.UUID, session: AsyncSession) -> list[Row[Any]]:
        result = await session.exec(select(Book).where(Book.user_uid == user_uid))
        return list(result.all())

    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Book | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        return result.first()

    async def create_book(self, book_data: BookCreateModel, user_uid: uuid.UUID, session: AsyncSession) -> Book:
        existing = await session.exec(
            select(Book).where(Book.title == book_data.title, Book.author == book_data.author, Book.user_uid == user_uid)
        )
        if existing.first():
            raise BookAlreadyExists()
        book = Book(**book_data.model_dump(), user_uid=user_uid)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def update_book(self, book_uid: uuid.UUID, book_update: BookUpdateModel, session: AsyncSession) -> Row[
                                                                                                                 Any] | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        book = result.first()
        if not book:
            return None
        for key, value in book_update.model_dump().items():
            setattr(book, key, value)
        book.updated_at = datetime.now()
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Row[Any] | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        book = result.first()
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return book


def get_book_service() -> IBookService:
    return BookService()
