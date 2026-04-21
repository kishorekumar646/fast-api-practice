from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import Account, AccountCreateModel, AccountUpdateModel, LoginModel
from .service import AccountService, LoginService
from src.errors import AccountNotFoundException

account_router = APIRouter()
account_service = AccountService()
login_service = LoginService()

@account_router.get(path='/accounts', response_model=List[Account])
async def get_all_accounts():
    try:
        accounts = await account_service.get_all_accounts()
        return accounts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@account_router.post(path='/account/login', response_model=Account, dependencies=[])
async def login_account(login_data: LoginModel):
    try:
        account = await login_service.login_account(login_data)
        return account
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@account_router.post(path='/account/signup', response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(account_data: AccountCreateModel):
    try:
        new_account = await account_service.add_account(account_data)
        return new_account
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@account_router.patch(path='/account/{account_uid}', response_model=Account, status_code=status.HTTP_202_ACCEPTED)
async def update_account(account_uid: str, account_data: AccountUpdateModel):
    try:
        updated_account = await account_service.update_account(account_uid=account_uid, account_update=account_data)
        return updated_account
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@account_router.delete('/account/{account_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_uid: str):
    try:
        await account_service.delete_account(account_uid=account_uid)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))