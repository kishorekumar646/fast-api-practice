import uuid
from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel


class IBookService(ABC):

    @abstractmethod
    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        pass

    @abstractmethod
    async def get_user_books(self, user_uid: uuid.UUID, session: AsyncSession) -> list[Book]:
        pass

    @abstractmethod
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Book | None:
        pass

    @abstractmethod
    async def create_book(self, book_data: BookCreateModel, user_uid: uuid.UUID, session: AsyncSession) -> Book:
        pass

    @abstractmethod
    async def update_book(self, book_uid: uuid.UUID, book_update: BookUpdateModel, session: AsyncSession) -> Book | None:
        pass

    @abstractmethod
    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession) -> Book | None:
        pass
