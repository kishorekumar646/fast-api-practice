import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.accounts.dependencies import AccessTokenBearer, RoleChecker

from .interfaces import IReviewService
from .schemas import ReviewCreateModel, ReviewUpdateModel, ReviewResponse
from .service import get_review_service

review_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@review_router.get("/", response_model=List[ReviewResponse], dependencies=[role_checker])
async def get_all_reviews(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    return await review_service.get_all_reviews(session)


@review_router.get("/book/{book_uid}", response_model=List[ReviewResponse], dependencies=[role_checker])
async def get_book_reviews(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    return await review_service.get_book_reviews(book_uid, session)


@review_router.post("/book/{book_uid}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_review(
    book_uid: uuid.UUID,
    data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    user_uid = uuid.UUID(token_data["user"]["user_uid"])
    return await review_service.create_review(book_uid, user_uid, data, session)


@review_router.get("/{review_uid}", response_model=ReviewResponse, dependencies=[role_checker])
async def get_review(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    review = await review_service.get_review(review_uid, session)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@review_router.patch("/{review_uid}", response_model=ReviewResponse, dependencies=[role_checker])
async def update_review(
    review_uid: uuid.UUID,
    data: ReviewUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    review = await review_service.update_review(review_uid, data, session)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@review_router.delete("/{review_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_review(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    review_service: IReviewService = Depends(get_review_service),
):
    deleted = await review_service.delete_review(review_uid, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
