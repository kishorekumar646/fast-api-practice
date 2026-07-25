import uuid
from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Review
from .schemas import ReviewCreateModel, ReviewUpdateModel


class IReviewService(ABC):

    @abstractmethod
    async def get_all_reviews(self, session: AsyncSession) -> list[Review]:
        pass

    @abstractmethod
    async def get_book_reviews(self, book_uid: uuid.UUID, session: AsyncSession) -> list[Review]:
        pass

    @abstractmethod
    async def get_review(self, review_uid: uuid.UUID, session: AsyncSession) -> Review | None:
        pass

    @abstractmethod
    async def create_review(
        self, book_uid: uuid.UUID, user_uid: uuid.UUID, data: ReviewCreateModel, session: AsyncSession
    ) -> Review:
        pass

    @abstractmethod
    async def update_review(
        self, review_uid: uuid.UUID, data: ReviewUpdateModel, session: AsyncSession
    ) -> Review | None:
        pass

    @abstractmethod
    async def delete_review(self, review_uid: uuid.UUID, session: AsyncSession) -> bool:
        pass
