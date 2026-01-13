from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.AuthController import AuthController
from app.schemas.auth_schema import Token, LoginRequest, RefreshTokenRequest
from config.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user with email and password, returns access and refresh tokens"
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.

    - **email**: User email address
    - **password**: User password

    Returns access token and refresh token for subsequent authenticated requests.
    """
    return await AuthController.login(login_data, db)


@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="Generate new access token using valid refresh token"
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token.

    - **refresh_token**: Valid refresh token

    Returns new access token and refresh token.
    """
    return await AuthController.refresh_token(refresh_data, db)
