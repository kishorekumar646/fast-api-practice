from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.db.redis import add_token_to_blocklist
from src.auth.schemas import UserCreateModel, UserLoginModel, TokenResponse, UserResponse
from src.auth.utils import verify_password, create_access_token, create_refresh_token
from src.accounts.dependencies import AccessTokenBearer, RefreshTokenBearer

from .interfaces import IUserService
from .service import get_user_service

auth_router = APIRouter()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
    user_service: IUserService = Depends(get_user_service),
):
    existing = await user_service.get_user_by_email(user_data.email, session)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = await user_service.create_user(user_data, session)
    return {
        "message": "Account created successfully",
        "uid": str(user.uid),
        "email": user.email,
        "username": user.username,
    }


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLoginModel,
    session: AsyncSession = Depends(get_session),
    user_service: IUserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(credentials.email, session)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_data = {"user_uid": str(user.uid), "email": user.email, "role": user.role}
    return TokenResponse(
        access_token=create_access_token(user_data),
        refresh_token=create_refresh_token(user_data),
        user=UserResponse(
            uid=str(user.uid),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        ),
    )


@auth_router.get("/refresh")
async def refresh_token(token_data: dict = Depends(RefreshTokenBearer())):
    user_data = token_data["user"]
    return {
        "access_token": create_access_token(user_data),
        "token_type": "bearer",
    }


@auth_router.post("/logout")
async def logout(token_data: dict = Depends(AccessTokenBearer())):
    await add_token_to_blocklist(token_data["jti"])
    return {"message": "Logged out successfully"}
