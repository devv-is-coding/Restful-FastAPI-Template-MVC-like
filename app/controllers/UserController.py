from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_db
from app.services.UserService import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.utils.dependencies import get_current_user, get_current_superuser
from app.models.User import User


class UserController:
    @staticmethod
    async def create_user(
        user_data: UserCreate, db: AsyncSession = Depends(get_db)
    ) -> UserResponse:
        """Create a new user"""
        user_service = UserService(db)
        return await user_service.create_user(user_data)

    @staticmethod
    async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> UserResponse:
        """Get user by ID"""
        user_service = UserService(db)
        return await user_service.get_user_by_id(user_id)

    @staticmethod
    async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_superuser),
    ) -> List[UserResponse]:
        """Get all users (superuser only)"""
        user_service = UserService(db)
        return await user_service.get_all_users(skip=skip, limit=limit)

    @staticmethod
    async def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> UserResponse:
        """Update user"""
        # Users can only update their own data unless they're superuser
        if user_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )

        user_service = UserService(db)
        return await user_service.update_user(user_id, user_data)

    @staticmethod
    async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_superuser),
    ) -> dict:
        """Delete user (superuser only)"""
        user_service = UserService(db)
        await user_service.delete_user(user_id)
        return {"message": "User deleted successfully"}

    @staticmethod
    async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
        """Get current user profile"""
        return UserResponse.model_validate(current_user)
