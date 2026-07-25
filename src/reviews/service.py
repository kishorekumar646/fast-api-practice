import uuid
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Review
from .interfaces import IReviewService
from .schemas import ReviewCreateModel, ReviewUpdateModel


class ReviewService(IReviewService):

    async def get_all_reviews(self, session: AsyncSession) -> list[Review]:
        result = await session.exec(select(Review))
        return list(result.all())

    async def get_book_reviews(self, book_uid: uuid.UUID, session: AsyncSession) -> list[Review]:
        result = await session.exec(select(Review).where(Review.book_uid == book_uid))
        return list(result.all())

    async def get_review(self, review_uid: uuid.UUID, session: AsyncSession) -> Review | None:
        result = await session.exec(select(Review).where(Review.uid == review_uid))
        return result.first()

    async def create_review(
        self, book_uid: uuid.UUID, user_uid: uuid.UUID, data: ReviewCreateModel, session: AsyncSession
    ) -> Review:
        review = Review(**data.model_dump(), book_uid=book_uid, user_uid=user_uid)
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review

    async def update_review(
        self, review_uid: uuid.UUID, data: ReviewUpdateModel, session: AsyncSession
    ) -> Review | None:
        review = await self.get_review(review_uid, session)
        if not review:
            return None
        for key, value in data.model_dump().items():
            setattr(review, key, value)
        review.updated_at = datetime.now()
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review

    async def delete_review(self, review_uid: uuid.UUID, session: AsyncSession) -> bool:
        review = await self.get_review(review_uid, session)
        if not review:
            return False
        await session.delete(review)
        await session.commit()
        return True


def get_review_service() -> IReviewService:
    return ReviewService()
