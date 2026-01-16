from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.UserController import UserController
from app.models.User import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.utils.dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_admin,
)
from config.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Register a new user account",
)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    - **email**: Valid email address (unique)
    - **username**: Username (unique, 3-50 characters)
    - **password**: Password (8-100 characters)
    - **first_name**: User's first name
    - **middle_name**: User's middle name (optional)
    - **last_name**: User's last name
    - **phone_number**: User's phone number
    - **phone_number2**: User's second phone number (optional)
    Returns the created user information.
    """
    return await UserController.create_user(user_data, db)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User Profile",
    description="Get authenticated user's profile information",
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current authenticated user's profile.

    Requires valid access token in Authorization header.

    Returns user profile information.
    """
    return await UserController.get_me(current_user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
    description="Retrieve user information by user ID",
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get user by ID.

    - **user_id**: User ID to retrieve

    Requires authentication.

    Returns user information.
    """
    return await UserController.get_user(user_id, db)


@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
    description="Retrieve all users (superuser only)",
)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Get all users (admin only).

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return

    Requires admin privileges.

    Returns list of all users.
    """
    return await UserController.get_all_users(skip, limit, db)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update User",
    description="Update user information",
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update user information.

    - **user_id**: User ID to update
    - **email**: New email (optional)
    - **username**: New username (optional)
    - **full_name**: New full name (optional)
    - **password**: New password (optional)

    Users can only update their own profile unless they are superuser.

    Returns updated user information.
    """
    return await UserController.update_user(user_id, user_data, db, current_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
    description="Delete user account (superuser only)",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Delete user (admin only).

    - **user_id**: User ID to delete

    Requires superuser privileges.

    Returns no content on success.
    """
    return await UserController.delete_user(user_id, db)
