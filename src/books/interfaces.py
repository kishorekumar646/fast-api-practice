from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel


class IBookService(ABC):

    @abstractmethod
    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        pass

    @abstractmethod
    async def get_book(self, book_uid: str, session: AsyncSession) -> Book:
        pass

    @abstractmethod
    async def add_book(self, book_data: BookCreateModel, user_uid: str, session: AsyncSession) -> Book:
        pass

    @abstractmethod
    async def update_book(self, book_uid: str, book_update: BookUpdateModel, session: AsyncSession) -> Book:
        pass

    @abstractmethod
    async def delete_book(self, book_uid: str, session: AsyncSession) -> None:
        pass
