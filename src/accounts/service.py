import uuid
from src.errors import AccountNotFoundException
from datetime import datetime
from fastapi.responses import JSONResponse
from .schemas import AccountCreateModel, AccountUpdateModel, Account, LoginModel

account_list = [
    Account(
        uid=uuid.uuid4(),
        username="john_doe",
        password="password123",
        email="john_doe@example.com",
        full_name="John Doe",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Account(
        uid=uuid.uuid4(),
        username="jane_smith",
        password="password456",
        email="jane_smith@example.com",
        full_name="Jane Smith",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Account(
        uid=uuid.uuid4(),
        username="kishore_kumar",
        password="password789",
        email="kishore_kumar@example.com",
        full_name="Kishore Kumar",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

class AccountService:

    async def get_all_accounts(self):
        return JSONResponse(content=[account.model_dump(mode='json') for account in account_list])

    async def add_account(self, account: AccountCreateModel):
        account_data = {
            "uid": uuid.uuid4(),
            "username": account.username,
            "email": account.email,
            "full_name": account.full_name,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        new_account = Account(**account_data)
        account_list.append(new_account)
        return JSONResponse(content=new_account.model_dump(mode='json'))
    
    async def update_account(self, account_uid: str, account_update: AccountUpdateModel):
        for account in account_list:
            if str(account.uid) == account_uid:
                account.username = account_update.username
                account.email = account_update.email
                account.full_name = account_update.full_name
                account.updated_at = datetime.now()
                return JSONResponse(content=account.model_dump(mode='json'))
        raise AccountNotFoundException()
    
    async def delete_account(self, account_uid: str):
        for account in account_list:
            if str(account.uid) == account_uid:
                account_list.remove(account)
                return JSONResponse(content={"detail": "Account deleted successfully"})
        raise AccountNotFoundException()
    
class LoginService:

    async def login_account(self, login_data: LoginModel):
        for account in account_list:
            if account.username == login_data.username and account.password == login_data.password:
                return JSONResponse(content=account.model_dump(mode='json'))
        raise AccountNotFoundException()