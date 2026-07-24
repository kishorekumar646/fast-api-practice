from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.db.redis import token_in_blocklist
from src.auth.utils import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


class TokenBearer:
    token_type: str = ""

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> dict:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        payload = decode_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if payload.get("type") != self.token_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Expected {self.token_type} token")
        if await token_in_blocklist(payload.get("jti", "")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
        return payload


class AccessTokenBearer(TokenBearer):
    token_type = "access"


class RefreshTokenBearer(TokenBearer):
    token_type = "refresh"


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, token_data: dict = Depends(AccessTokenBearer())
    ) -> dict:
        user = token_data.get("user", {})
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return token_data
