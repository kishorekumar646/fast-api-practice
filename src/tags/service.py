import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Tag, Book, BookTag
from .schemas import TagCreateModel


class TagService:

    async def get_all_tags(self, session: AsyncSession) -> list[Tag]:
        result = await session.exec(select(Tag))
        return list(result.all())

    async def get_tag(self, tag_uid: uuid.UUID, session: AsyncSession) -> Tag | None:
        result = await session.exec(select(Tag).where(Tag.uid == tag_uid))
        return result.first()

    async def create_tag(self, data: TagCreateModel, session: AsyncSession) -> Tag:
        result = await session.exec(select(Tag).where(Tag.name == data.name))
        existing = result.first()
        if existing:
            return existing
        tag = Tag(name=data.name)
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag

    async def delete_tag(self, tag_uid: uuid.UUID, session: AsyncSession) -> bool:
        tag = await self.get_tag(tag_uid, session)
        if not tag:
            return False
        await session.delete(tag)
        await session.commit()
        return True

    async def add_tag_to_book(
        self, book_uid: uuid.UUID, tag_uid: uuid.UUID, session: AsyncSession
    ) -> Book | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        book = result.first()
        tag = await self.get_tag(tag_uid, session)
        if not book or not tag:
            return None
        book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def remove_tag_from_book(
        self, book_uid: uuid.UUID, tag_uid: uuid.UUID, session: AsyncSession
    ) -> Book | None:
        result = await session.exec(select(Book).where(Book.uid == book_uid))
        book = result.first()
        tag = await self.get_tag(tag_uid, session)
        if not book or not tag:
            return None
        book.tags = [t for t in book.tags if t.uid != tag_uid]
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
