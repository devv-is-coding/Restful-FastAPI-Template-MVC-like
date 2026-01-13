from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.UserRepository import UserRepository
from app.schemas.auth_schema import LoginRequest, Token
from app.utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def login(self, login_data: LoginRequest) -> Token:
        """Authenticate user and return tokens"""
        user = await self.user_repo.get_by_email(login_data.email)

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        # Create tokens
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username}
        )
        refresh_token = create_refresh_token(data={"user_id": user.id})

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    async def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token"""
        payload = decode_token(refresh_token)

        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Create new tokens
        new_access_token = create_access_token(
            data={"user_id": user.id, "username": user.username}
        )
        new_refresh_token = create_refresh_token(data={"user_id": user.id})

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
