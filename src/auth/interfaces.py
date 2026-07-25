from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from .schemas import UserCreateModel


class IUserService(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_uid(self, uid: str, session: AsyncSession) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        pass
