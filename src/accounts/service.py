import uuid
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.errors import AccountNotFoundException
from .schemas import AccountUpdateModel


class AccountService:

    @staticmethod
    async def get_all_accounts(session: AsyncSession) -> list[User]:
        result = await session.exec(select(User))
        return list(result.all())

    @staticmethod
    async def get_account(user_uid: uuid.UUID, session: AsyncSession) -> User:
        result = await session.exec(select(User).where(User.uid == user_uid))
        user = result.first()
        if not user:
            raise AccountNotFoundException()
        return user

    async def update_account(
        self, user_uid: uuid.UUID, update_data: AccountUpdateModel, session: AsyncSession
    ) -> User:
        user = await self.get_account(user_uid, session)
        for key, value in update_data.model_dump().items():
            setattr(user, key, value)
        user.updated_at = datetime.now()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_account(self, user_uid: uuid.UUID, session: AsyncSession) -> None:
        user = await self.get_account(user_uid, session)
        await session.delete(user)
        await session.commit()
