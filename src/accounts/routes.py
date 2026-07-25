import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.errors import AccountNotFoundException

from .interfaces import IAccountService
from .schemas import AccountUpdateModel, AccountResponse
from .service import get_account_service
from .dependencies import AccessTokenBearer, RoleChecker

account_router = APIRouter()
access_token_bearer = AccessTokenBearer()
admin_only = RoleChecker(["admin"])


@account_router.get("/", response_model=List[AccountResponse])
async def get_all_accounts(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(admin_only),
    account_service: IAccountService = Depends(get_account_service),
):
    return await account_service.get_all_accounts(session)


@account_router.get("/me", response_model=AccountResponse)
async def get_my_account(
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(access_token_bearer),
    account_service: IAccountService = Depends(get_account_service),
):
    user_uid = uuid.UUID(token_data["user"]["user_uid"])
    try:
        return await account_service.get_account(user_uid, session)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@account_router.get("/{user_uid}", response_model=AccountResponse)
async def get_account(
    user_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
    account_service: IAccountService = Depends(get_account_service),
):
    try:
        return await account_service.get_account(user_uid, session)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@account_router.patch("/{user_uid}", response_model=AccountResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_account(
    user_uid: uuid.UUID,
    update_data: AccountUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(access_token_bearer),
    account_service: IAccountService = Depends(get_account_service),
):
    try:
        return await account_service.update_account(user_uid, update_data, session)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@account_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(admin_only),
    account_service: IAccountService = Depends(get_account_service),
):
    try:
        await account_service.delete_account(user_uid, session)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
