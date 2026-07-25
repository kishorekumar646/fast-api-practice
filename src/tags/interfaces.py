import uuid
from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book, Tag
from .schemas import TagCreateModel


class ITagService(ABC):

    @abstractmethod
    async def get_all_tags(self, session: AsyncSession) -> list[Tag]:
        pass

    @abstractmethod
    async def create_tag(self, data: TagCreateModel, session: AsyncSession) -> Tag:
        pass

    @abstractmethod
    async def delete_tag(self, tag_uid: uuid.UUID, session: AsyncSession) -> bool:
        pass

    @abstractmethod
    async def add_tag_to_book(
        self, book_uid: uuid.UUID, tag_uid: uuid.UUID, session: AsyncSession
    ) -> Book | None:
        pass

    @abstractmethod
    async def remove_tag_from_book(
        self, book_uid: uuid.UUID, tag_uid: uuid.UUID, session: AsyncSession
    ) -> Book | None:
        pass
