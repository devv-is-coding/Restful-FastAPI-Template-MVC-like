from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from app.services.AuthService import AuthService
from app.schemas.auth_schema import LoginRequest, Token, RefreshTokenRequest


class AuthController:
    @staticmethod
    async def login(
        login_data: LoginRequest, db: AsyncSession = Depends(get_db)
    ) -> Token:
        """Login user"""
        auth_service = AuthService(db)
        return await auth_service.login(login_data)

    @staticmethod
    async def refresh_token(
        refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
    ) -> Token:
        """Refresh access token"""
        auth_service = AuthService(db)
        return await auth_service.refresh_token(refresh_data.refresh_token)
