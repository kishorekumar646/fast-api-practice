from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import hash_password


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        result = await session.exec(select(User).where(User.email == email))
        return result.first()

    async def get_user_by_uid(self, uid: str, session: AsyncSession) -> User | None:
        import uuid
        result = await session.exec(select(User).where(User.uid == uuid.UUID(uid)))
        return result.first()

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=hash_password(user_data.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
