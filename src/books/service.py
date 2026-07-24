import uuid
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.errors import BookNotFoundException
from .schemas import BookCreateModel, BookUpdateModel


class BookService:

    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        result = await session.exec(select(Book))
        return list(result.all())

    async def get_user_books(self, user_uid: uuid.UUID, session: AsyncSession) -> list[Book]:
        result = await session.exec(select(Book).where(Book.user_uid == user_uid))
        return list(result.all())

    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Book | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        return result.first()

    async def create_book(self, book_data: BookCreateModel, user_uid: uuid.UUID, session: AsyncSession) -> Book:
        book = Book(**book_data.model_dump(), user_uid=user_uid)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def update_book(self, book_uid: uuid.UUID, book_update: BookUpdateModel, session: AsyncSession) -> Book | None:
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

    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Book | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        book = result.first()
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return book
