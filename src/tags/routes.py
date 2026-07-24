import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.accounts.dependencies import AccessTokenBearer, RoleChecker
from src.books.schemas import BookDetailModel
from .schemas import TagCreateModel, TagResponse
from .service import TagService

tag_router = APIRouter()
tag_service = TagService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))
admin_checker = RoleChecker(["admin"])


@tag_router.get("/", response_model=List[TagResponse], dependencies=[role_checker])
async def get_all_tags(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    return await tag_service.get_all_tags(session)


@tag_router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(admin_checker),
):
    return await tag_service.create_tag(data, session)


@tag_router.delete("/{tag_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(admin_checker),
):
    deleted = await tag_service.delete_tag(tag_uid, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")


@tag_router.post("/book/{book_uid}/{tag_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def add_tag_to_book(
    book_uid: uuid.UUID,
    tag_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    book = await tag_service.add_tag_to_book(book_uid, tag_uid, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book or tag not found")
    return book


@tag_router.delete("/book/{book_uid}/{tag_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def remove_tag_from_book(
    book_uid: uuid.UUID,
    tag_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    book = await tag_service.remove_tag_from_book(book_uid, tag_uid, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book or tag not found")
    return book
