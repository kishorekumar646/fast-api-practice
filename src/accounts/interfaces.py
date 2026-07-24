import uuid
from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from .schemas import AccountUpdateModel


class IAccountService(ABC):

    @abstractmethod
    async def get_all_accounts(self, session: AsyncSession) -> list[User]:
        pass

    @abstractmethod
    async def get_account(self, user_uid: uuid.UUID, session: AsyncSession) -> User:
        pass

    @abstractmethod
    async def update_account(self, user_uid: uuid.UUID, update_data: AccountUpdateModel, session: AsyncSession) -> User:
        pass

    @abstractmethod
    async def delete_account(self, user_uid: uuid.UUID, session: AsyncSession) -> None:
        pass
